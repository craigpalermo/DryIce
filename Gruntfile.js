module.exports = function(grunt) {
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-commands');
    
    grunt.initConfig({
        watch: {
            livereload: {
                options: { livereload: true },
                files: ['DryIce/static/css/*', 
                        'DryIce/static/js/*',
                        'DryIce/templates/*',
                       ]
            }
        },
        command: {
            run_cmd: {
                cmd: ['python manage.py runserver 0.0.0.0:8000']
            }
        }
    });
};
