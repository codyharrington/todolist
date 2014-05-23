/**
 * Created by cody on 23/05/14.
 */
module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON("package.json"),
        concat: {
            dist: {
                src: ["js/**/*.js"],
                dest: "min/todolist.cat.js"
            }
        },
        uglify: {
            dist: {
                files: {
                    "min/todolist.min.js": ["min/todolist.cat.js"]
                }
            }
        },
        cssmin: {
            combine: {
                files: {
                    "min/todolist.cat.css": ["css/**/*.css"]
                }
            },
            minify: {
                src: ["min/todolist.cat.css"],
                dest: "min/",
                ext: ".min.css"
            }
        },
        watch: {
            files: ["js/*.js", "css/*.css"],
            tasks: ["uglify", "jshint", "qunit"]
        },
        qunit: {
            files: ["js/test/**/*.html"]
        },
        jshint: {
            files: ["Gruntfile.js", "js/*.js", "js/test/**/*.js"]
        }
    });

    grunt.loadNpmTasks("grunt-contrib-uglify");
    grunt.loadNpmTasks("grunt-contrib-concat");
    grunt.loadNpmTasks("grunt-contrib-jshint");
    grunt.loadNpmTasks("grunt-contrib-cssmin");
    grunt.loadNpmTasks("grunt-contrib-watch");
    grunt.loadNpmTasks("grunt-contrib-qunit");

    grunt.registerTask("default", ["jshint", "qunit", "concat", "uglify", "cssmin" ]);
}