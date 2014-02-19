module.exports = function(grunt) {
    grunt.loadNpmTasks('grunt-contrib-watch');
    
    grunt.initConfig({
        watch: {
            livereload: {
                options: { livereload: true },
                files: ['DryIce/static/css/*', 
                        'DryIce/static/js/*',
                        'DryIce/templates/*',
                       ]
            }
        }
    });

    grunt.registerTask('server', 'Start a custom web server', function() {
        grunt.log.writeln('Started web server on port 3000');
        require('./app.js').listen(3000);
    });
};
