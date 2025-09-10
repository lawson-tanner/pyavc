from .file import AVCFile
import os


def convert(filepath, output_dir, output_name: str = None, text_width: int = 80, font_size: int = 12, font_name: str = "Open Sans", white_bg: bool = False, show_row_colors: bool = True, left_margin: int = 40, text_width_px: int = 512, show_frames: bool = True, interpolate_position: bool = False, show_all_takes: bool = True, show_line_numbers: bool = True, word_wrap: bool = True, hold_slates_onscreen: bool = False, take_color: int = 1):
    """Converts a DOCX or TXT file into an AVC file for use in Avid Media Composer.

    This function processes a text-based document and renders it as an
    AVC file with extensive formatting and display options. All display and formatting options mirror Avid Media Composer's Script setting dialog.

    Args:
        filepath (str): The full path to the source DOCX or TXT file.
        output_dir (str): The directory where the output AVC file will be saved.
        output_name (str, optional): The desired name for the output file. 
            If None, a name is automatically generated from the input file. 
            Defaults to None.
        text_width (int, optional): The number of characters to include before splitting into a newline. Defaults to 80 chars. 
        font_size (int, optional): The font size for the text. Defaults to 12. Maximum 255px.
        font_name (str, optional): The name of the font to be used. 
            Defaults to "Open Sans". If an invalid font is supplied, Avid will substitute it with the system default.
        white_bg (bool, optional): If True, the window background will be white. 
            If False, the window background will defer to user settings.
        show_row_colors (bool, optional): If True, rows will have alternating 
            background colors for readability. Defaults to True.
        left_margin (int, optional): The size of the left margin in pixels. 
            Defaults to 40.
        text_width_px (int, optional): The width of the text layout area in pixels.
            Defaults to 512. Minimum 128px, maximum 5120px
        show_frames (bool, optional): If True, frame counter information is
            displayed on the video. Defaults to True.
        interpolate_position (bool, optional): If True, Avid will allow you to add your own sync marks.
        show_all_takes (bool, optional): If True, all takes are displayed. If 
            False, only the primary take is shown. Defaults to True.
        show_line_numbers (bool, optional): If True, line numbers are displayed
            alongside the text. Defaults to True.
        word_wrap (bool, optional): If True, long lines of text will wrap to
            fit within the specified text_width. Defaults to True.
        hold_slates_onscreen (bool, optional): If True, slates will remain on
            screen until the next slate appears. Defaults to False.
        take_color (int, optional): An integer (1-22) to select a highlight
            color for takes. Please check the README file for specific
            guidance on the color-to-integer mapping. Defaults to 1.
    
    Raises:
        FileNotFoundError: If the file specified in `filepath` does not exist.
        ValueError: If `take_color` is outside the valid range of 1-22.
        AVCException: If any items are outside the specified minimum and maximum range.

    Returns:
        output_filepath: The location of the generated AVC file, if successful.
    """
    
    if not os.path.exists(filepath):
            raise FileNotFoundError(f"The input file '{filepath}' does not exist.")
        
    if not (filepath.lower().endswith('.txt') or filepath.lower().endswith('.docx')):
        raise ValueError(f"The input file '{filepath}' must be a .txt or .docx file.")
        
        # Check if the output directory exists
    if not os.path.exists(output_dir):
        raise NotADirectoryError(f"The output directory '{output_dir}' does not exist or is not a directory.")
        
    avc = AVCFile(filepath, output_dir, output_name, text_width, font_size, font_name, white_bg, show_row_colors, left_margin, text_width_px, show_frames, interpolate_position, show_all_takes, show_line_numbers, word_wrap, hold_slates_onscreen, take_color) 

    try:
        returned_filepath = avc.create()
        return returned_filepath

    except Exception as e:
        print(f"There was an error: {e}")
