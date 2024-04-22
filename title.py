from PIL import Image, ImageDraw, ImageFont, ImageStat


def find_text_color(image_path, light_colour, dark_colour):
    # Open the image
    with Image.open(image_path) as image:
        text_area = ( round(image.width * 0.2), round(image.height * 0.05), round(image.width * 0.8), round(image.height * 0.2 ))

        # Crop the image to the specified text area
        cropped_image = image.crop(text_area)

        # Calculate the average color of the cropped area
        avg_color = ImageStat.Stat(cropped_image).mean

        # Convert the average color to RGB values
        avg_r, avg_g, avg_b = avg_color[:3]

        # Calculate the brightness of the average color
        brightness = (avg_r + avg_g + avg_b) / 3

        if brightness > 127:
            return dark_colour
        else:
            return light_colour

def add_text_to_image(image_path, title, author, title_font_path, author_font_path, title_color, author_color):
    # Load the image
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)

        # Define maximum width for text based on image size
        max_width = img.width * 0.8  # 80% of the image width
        margin = (img.width - max_width) / 2

        # Function to scale font size
        def get_font_size(text, font_path, max_width):
            font_size = 1  # Starting font size
            font = ImageFont.truetype(font_path, font_size)
            while font.getlength(text) < max_width:
                font_size += 1
                font = ImageFont.truetype(font_path, font_size)
            return ImageFont.truetype(font_path, font_size - 1)  # step back to keep within bounds

        # Get scaled fonts
        title_font = get_font_size(title, title_font_path, max_width)
        author_font = get_font_size(author, author_font_path, max_width * 0.6)  # Slightly smaller width for author

        # Calculate text positions
        title_bbox = title_font.getbbox(title)
        author_bbox = author_font.getbbox(author)

        title_width = title_bbox[2] - title_bbox[0]
        author_width = author_bbox[2] - author_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]
        author_height = author_bbox[3] - author_bbox[1]

        title_x = (img.width - title_width) / 2
        title_y = img.height * 0.05  # 5% from the top

        author_x = (img.width - author_width) / 2
        author_y = title_y + title_height + 20  # 20 pixels below the title

        # Add text to image
        draw.text((title_x, title_y), title, font=title_font, fill=title_color)
        draw.text((author_x, author_y), author, font=author_font, fill=author_color)

        # Save the edited image
        img.save("amended_"+image_path)


if __name__ == '__main__':
    # Example usage
    image_path = 'swordswoman.png'
    title = "Gideon the Ninth"
    author = "Tamsyn Muir"
    title_font_path = "arial.ttf"  # Path to a TTF font file for the title
    author_font_path = "arial.ttf"  # Path to a TTF font file for the author

    color = find_text_color(image_path, "mistyrose", "navy")

    add_text_to_image(image_path, title, author, title_font_path, author_font_path, color, color)
