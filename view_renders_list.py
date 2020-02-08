import sublime, sublime_plugin, os

# super + alt + 7

class ViewRendersListCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    all_renders = self.view.find_all(' render ')
    files       = []

    for d in all_renders:
      line        = self.view.line(d)
      line_text   = self.view.substr(line)
      view_name   = self.find_view_from_view(line_text.split('\'')[1])
      if len(view_name) > 0:
        files.append(view_name)

    self.files = files
    sublime.active_window().show_quick_panel(files, self.open_file)

  def find_view_from_view(self, file_name):
    if len(file_name) > 0:
      source          = self.view.file_name()
      source_path     = os.path.dirname(source)
      rails_view_path = os.path.dirname(source_path)

      if '/' in file_name:
        split_file_name = file_name.split('/')

        if len(split_file_name) == 2:
          new_file_name = split_file_name[0] + '/_' + split_file_name[1]
        else:
          new_file_name = split_file_name[0] + '/' + split_file_name[1] + '/_' + split_file_name[2]

        if split_file_name[0] in rails_view_path:
          file_path = rails_view_path.replace(split_file_name[0], '') + '/' + new_file_name
        else:
          if rails_view_path.split('/')[-2] == 'views':
            file_path = rails_view_path.replace(rails_view_path.split('/')[-1], '') + '/' + new_file_name
          else:
            file_path = rails_view_path + '/' + new_file_name
      else:
        new_file_name = file_name
        file_path = source_path + '/_' + new_file_name

      extensions = ['haml', 'html.erb', 'html.slim', 'pdf.haml', 'pdf.erb', 'pdf.haml']

      for i in extensions:
        if os.path.exists(file_path + '.' + i):
          return file_path + '.' + i

  def open_file(self, index):
    if index >= 0:
      sublime.active_window().open_file(os.path.join(self.files[index]))