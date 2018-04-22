var app = new Vue({
    mixins: [utils],
    el: '#app',
    data: {
        token: Cookies.get('auth_token'),
        is_admin: (Cookies.get('is_admin')=='true'),
        branches: [],
        categories: [],
        students: [],
        selectedCategories: [],
        selectedBranches: [],
        selectedStudents: [],
        month: '',
        loading: false,
        taskCount: 0,
        error: '',

        initialized: false,
    },
    created(){
        console.log('created')
        this.load(['students', 'branches', 'categories'])
    },
    updated(){
        console.log('updated')
        if(!this.initialized && !this.loading){
            console.log('initialized')
            var dom = $(this.$el)
            dom.find('.dropdown').dropdown()
            dom.find('#month').calendar({
                type: 'month',
                closable: true,
                maxDate: new Date(),
                onChange: this.setMonth,
            })
            this.initialized = true
        }
    },
    methods: {
        toggleStudentSelection(student){
            var index = this.selectedStudents.indexOf(student)
            if(index ==-1){
                this.selectedStudents.push(student)
            } else {
                this.selectedStudents.splice(index, 1)
            }
        },
        setMonth(date, text, mode){
            this.month = moment(date).format('MMMM YYYY')
        },
        exportReport(){
            this.loading = true
            this.error = ''
            var vm = this
            var url = '/api/exportReport'
            var students = this.selectedStudents
            if (students.length == 0)
               students = this.filteredStudents
           studentIds = []
           students.forEach((student) => {
            studentIds.push(student.id)
        })
           vm.month = vm.month || moment().format('MMMM YYYY')
           var postData = {
            month: vm.month,
            students: studentIds,
            categories: vm.selectedCategories,
            branches: vm.selectedBranches,
        }
        console.log(postData)
        var config = this.getHeaders()
        config.responseType = 'blob'
        this.$http.post(url, postData, config)
        .then(response => {
            this.loading = false
            var blob = new Blob([response.data])
            var link = document.createElement('a')
            link.href = window.URL.createObjectURL(blob)
            link.download = 'Report ' + vm.month + '.pdf'
            link.click()
        },
        error => {
            this.loading = false
            this.error = 'Error occured'
            console.log(error)
        })
    }
},
computed: {
    filteredStudents(){
        var vm = this
        return this.students.filter(student => {
            return (vm.selectedCategories.length == 0 || vm.selectedCategories.indexOf(student.category) != -1) &&
            (vm.selectedBranches.length == 0 || vm.selectedBranches.indexOf(student.branch) != -1)
        })
    }
}
})