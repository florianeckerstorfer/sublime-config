import sublime
import sublime_plugin
import os


class Pref:
    @staticmethod
    def load():
        settings = sublime.load_settings('subfony.sublime-settings')
        Pref.php_bin = settings.get('php_bin', '/usr/bin/php')
        Pref.console_bin = settings.get('console_bin', 'app/console')
        Pref.src_dir = settings.get('src_dir', 'src')


st_version = 2
if sublime.version() == '' or int(sublime.version()) > 3000:
    st_version = 3

if st_version == 2:
    Pref.load()


def plugin_loaded():
    Pref.load()


class SubfonyGenerateBundleCommand(sublime_plugin.WindowCommand):
    INPUT_PANEL_CAPTION = 'Namespace:'
    output_view = ''
    global THEME

    def run(self):
        self.window.show_input_panel(self.INPUT_PANEL_CAPTION, '', self.on_done, None, None)
        self.view = self.window.active_view()

    def on_done(self, text):
        if not self.view or not self.view.file_name():
            sublime.status_message('A file must be open. Sorry.')
            return
        cwd = os.path.dirname(self.view.file_name())
        while not os.path.exists(cwd + '/app') or cwd == '/' or cwd == '':
            cwd = os.path.dirname(cwd)

        if cwd == '/' or cwd == '':
            sublime.status_message('You\'re not in a Symfony2 application.')
            return

        cmd = [Pref.php_bin, Pref.console_bin, 'generate:bundle', '--dir=' + Pref.src_dir, '--namespace=' + text, '--no-interaction']
        self.run_shell_command(cmd, cwd)

    def run_shell_command(self, command, working_dir):
        if not command:
            return False
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


class ShowInPanel:

    def __init__(self, window):
        self.window = window

    def display_results(self):
        self.panel = self.window.get_output_panel("exec")
        self.window.run_command("show_panel", {"panel": "output.exec"})
