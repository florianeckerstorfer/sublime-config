import sublime
import sublime_plugin
import thread
import subprocess
import os
import functools

st_version = 2
if sublime.version() == '' or int(sublime.version()) > 3000:
    st_version = 3


class ShowInPanel:

    def __init__(self, window):
        self.window = window

    def display_results(self):
        self.panel = self.window.get_output_panel("exec")
        self.window.run_command("show_panel", {"panel": "output.exec"})
        # self.panel.settings().set("color_scheme", THEME)
        # self.panel.set_syntax_file(SYNTAX)
        # if HIDE_PANEL:
            # self.window.run_command("hide_panel")
            # self.panel.settings().set("color_scheme", THEME)


class SubfonyGenerateBundleCommand(sublime_plugin.WindowCommand):
    INPUT_PANEL_CAPTION = 'Namespace:'
    output_view = ''
    global THEME

    def run(self):
        self.window.show_input_panel(self.INPUT_PANEL_CAPTION, '', self.on_done, None, None)
        self.view = self.window.active_view()

    def on_done(self, text):
        cmd = ['/usr/local/opt/php54/bin/php', 'app/console', 'generate:bundle', '--dir=src', '--namespace=' + text, '--no-interaction']

        self.run_shell_command(cmd, '/Users/florian/Workspace/playground/subfony')

    def run_shell_command(self, command, working_dir):
        if not command:
            return False
        sublime.status_message(' '.join(command))
        # if BEFORE_CALLBACK:
        #     os.system(BEFORE_CALLBACK)
        # if AFTER_CALLBACK:
        #     command += " ; " + AFTER_CALLBACK
        # self.save_test_run(command, working_dir)
        # if COMMAND_PREFIX:
        #     command = COMMAND_PREFIX + ' ' + command
        self.view.window().run_command("exec", {
            "cmd": command,
            "shell": False,
            "working_dir": working_dir,
            "file_regex": ""
        })
        self.display_results()
        return True

    def display_results(self):
        display = ShowInPanel(self.window)
        display.display_results()

    def window(self):
        return self.view.window()
