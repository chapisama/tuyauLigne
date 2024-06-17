from tuyauLigneSP import tuyauligne_import as tli
from tuyauLigneSP import tuyauligne_export as tle
import substance_painter.ui

plugin_widgets = []


def start_plugin():
    """
    Start the plugin by creating and displaying the UI, and storing the widget for cleanup.
    """
    import_widget = tli.create_ui()
    export_widget = tle.create_ui()

    # Add this widget as a dock to the interface
    substance_painter.ui.add_dock_widget(import_widget)
    substance_painter.ui.add_dock_widget(export_widget)
    # Store added widget for proper cleanup when stopping the plugin
    plugin_widgets.append(import_widget)
    plugin_widgets.append(export_widget)


def close_plugin():
    """
    Close the plugin by removing all UI elements added to the interface.
    """
    # Remove all widgets that have been added to the UI
    for widget in plugin_widgets:
        substance_painter.ui.delete_ui_element(widget)

    plugin_widgets.clear()


if __name__ == "__main__":
    start_plugin()
