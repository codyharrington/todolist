/**
 * Created by cody on 23/05/14.
 */
module.exports = function (grunt) {
    var jquery_js = "bower_components/jquery/dist/jquery.min.js";
    var jquery_ui_js = "bower_components/jquery-ui/ui/minified/jquery-ui.min.js";
    var jquery_validate_js = "bower_components/jquery-validation/dist/jquery.validate.min.js";
    var bootstrap_js = "bower_components/bootstrap/dist/js/bootstrap.min.js";

    var js_libs = [jquery_js, jquery_ui_js, jquery_validate_js, bootstrap_js];

    var jquery_ui_css = "bower_components/jquery-ui/themes/ui-darkness/jquery-ui.min.css";
    var bootstrap_css = "bower_components/bootstrap/dist/css/bootstrap.min.css";
    var bootstrap_theme_css = "bower_components/bootstrap/dist/css/bootstrap-theme.min.css";

    var css_libs = [jquery_ui_css, bootstrap_css, bootstrap_theme_css];

    grunt.initConfig({
        pkg: grunt.file.readJSON("package.json"),
        clean: {
            js: ["js/libs/**/*"],
            css: ["css/libs/**/*"],
            build: ["build/*"]
        },
        bower: {
            install: {
                options: {
                    install: true,
                    copy: false
                }
            }
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
            options: {
                stripBanners: true
            },
            dist: {
                src: ["js/**/*.js", "!js/test/*", "!js/libs/*"],
                dest: "build/todolist.cat.js"
            }
        },
        uglify: {
            dist: {
                files: {
                    "build/todolist.min.js": ["build/todolist.cat.js"]
                }
            }
        },
        cssmin: {
            combine: {
                files: {
                    "build/todolist.cat.css": ["css/**/*.css", "!css/libs/*"]
                }
            },
            minify: {
                src: ["build/todolist.cat.css"],
                dest: "build/todolist.min.css"
            }
        },
        watch: {
            files: ["js/*.js", "css/*.css"],
            tasks: ["concat", "uglify", "cssmin", "jshint", "qunit"]
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
    grunt.loadNpmTasks("grunt-contrib-clean");
    grunt.loadNpmTasks("grunt-contrib-copy");
    grunt.loadNpmTasks("grunt-bower-task");

    //grunt.loadNpmTasks("grunt-contrib-qunit");

    grunt.registerTask("test", ["jshint", "qunit"]);
    grunt.registerTask("default", ["clean", "bower", "copy", "jshint", "concat", "uglify", "cssmin" ]);
};