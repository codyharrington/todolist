/**
 * Created by cody on 23/05/14.
 */
module.exports = function (grunt) {
    var jquery_js = "node_modules/jquery/dist/jquery.min.js";
    var jquery_ui_js = "node_modules/jquery-ui/jquery-ui.js";
    var bootstrap_js = "node_modules/twitter-bootstrap-3.0.0/dist/js/bootstrap.min.js";

    var js_libs = [jquery_js, jquery_ui_js, bootstrap_js];

    var jquery_ui_css = "node_modules/jquery-ui/themes/ui-darkness/jquery-ui.min.css";
    var bootstrap_css = "node_modules/twitter-bootstrap-3.0.0/dist/css/bootstrap.min.css";
    var bootstrap_theme_css = "node_modules/twitter-bootstrap-3.0.0/dist/css/bootstrap-theme.min.css";

    var css_libs = [jquery_ui_css, bootstrap_css, bootstrap_theme_css];

    grunt.initConfig({
        pkg: grunt.file.readJSON("package.json"),
        clean: {
            js: ["js/libs/**/*"],
            css: ["css/libs/**/*"],
            min: ["min/*"]
        },
        copy: {
            main: {
                files: [
                    {expand: true, flatten: true, src: js_libs, dest: "js/libs/" },
                    {expand: true, flatten: true, src: css_libs, dest: "css/libs/" }
                ]
            }
        },
        concat: {
            dist: {
                src: ["js/**/*.js", "!js/test/*"],
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
                dest: "min/todolist.min.css"
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
    grunt.loadNpmTasks("grunt-contrib-copy");
    grunt.loadNpmTasks("grunt-contrib-clean");
//    grunt.loadNpmTasks("grunt-contrib-qunit");

    grunt.registerTask("test", ["jshint", "qunit"]);
    grunt.registerTask("default", ["clean", "copy", "jshint", "concat", "uglify", "cssmin" ]);
};