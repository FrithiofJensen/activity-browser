# -*- coding: utf-8 -*-
import brightway2 as bw
from PySide2 import QtCore, QtWidgets
from activity_browser.ui.widgets.dialog import ProjectDeletionDialog
from activity_browser.signals import signals


def test_new_project(qtbot, ab_app, monkeypatch):
    qtbot.waitForWindowShown(ab_app.main_window)
    monkeypatch.setattr(
        QtWidgets.QInputDialog, "getText",
        staticmethod(lambda *args, **kwargs: ("pytest_project_del", True))
    )
    project_tab = ab_app.main_window.left_panel.tabs['Project']
    qtbot.mouseClick(
        project_tab.projects_widget.new_project_button,
        QtCore.Qt.LeftButton
    )
    assert bw.projects.current == 'pytest_project_del'


def test_change_project(qtbot, ab_app):
    qtbot.waitForWindowShown(ab_app.main_window)
    assert bw.projects.current == 'pytest_project_del'
    project_tab = ab_app.main_window.left_panel.tabs['Project']
    combobox = project_tab.projects_widget.projects_list
    assert 'default' in bw.projects
    assert 'default' in combobox.project_names
    combobox.activated.emit(combobox.project_names.index('default'))
    assert bw.projects.current == 'default'
    combobox.activated.emit(combobox.project_names.index('pytest_project_del'))
    assert bw.projects.current == 'pytest_project_del'


def test_delete_project(qtbot, ab_app, monkeypatch):
    qtbot.waitForWindowShown(ab_app.main_window)
    assert bw.projects.current == 'pytest_project_del'

    monkeypatch.setattr(ProjectDeletionDialog, 'exec_', lambda self: ProjectDeletionDialog.Accepted)

    project_tab = ab_app.main_window.left_panel.tabs['Project']

    with qtbot.waitSignal(signals.change_project, timeout=5*1000):  # 5 seconds
        qtbot.mouseClick(
            project_tab.projects_widget.delete_project_button,
            QtCore.Qt.LeftButton
        )

    assert bw.projects.current == 'default'
