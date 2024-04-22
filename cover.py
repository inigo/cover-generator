from goodreads import get_book_info
from title import add_text_to_image, find_text_color
import openai
import json
import requests
from secrets import api_key

openai.api_key = api_key()
client = openai.OpenAI(api_key=openai.api_key)

system_prompt = """
    You are a book cover designer. You create appropriate images for book covers, based on the style, genre and description of the book. You recognize that different genres of book have different expectations about the cover. However, you purely create the image, you never add any text to it, because that is someone else's job.
    
    I will give you a book title, author, description and genres.
    
    From the genre, you will identify an art style that is appropriate for the book cover.
    
    From the description, and anything you already know about the author, you will identify four key themes in the book, that you will express as a word or a short phrase.
    
    Then, from that list, you will identify the three themes that will work best as theme prompts for an artist.
    
    For each theme, you will create an image prompt suitable for using with DALL-E to create a book cover for the book, based on that theme, and the art style. This should
    focus on only one or two striking images for each book. You will never include the information that this is for a book cover in the prompt. Please provide plenty of detail in the prompt. 
    
    You will then identify the typeface most suitable for the book genre from this list: arial.ttf, times.ttf, cour.ttf, verdana.ttf, calibri.ttf, segoeui.ttf, tahoma.ttf, georgia.ttf, comic.ttf, impact.ttf
    
    And then identify two appropriate colors for the book title text based on the art style, one light and one dark, using standard HTML color names. List the light one first. For example,
    for a romance, you might list title_color: ['mistyrose', 'fuchsia'],

    You will return a result in this JSON format:
    
    {
      art_style: 'aaa',
      typeface: 'arial.ttf',
      title_color: ['azure', 'navy'],
      themes: ['xxx', 'yyy', 'zzz'],
      prompts: [
        {
            theme: 'xxx',
            prompt: 'First prompt based on xxx and the art style'
        },
        {
            theme: 'yyy',
            prompt: 'Second prompt based on yyy and the art style'
        },
        {
            theme: 'zzz',
            prompt: 'Third prompt based on zzz and the art style'
        }
      ]
    
      I will now provide the book information in a different JSON format. Here is the book information:        
    
    """

def create_description(prompt):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message


def generate_image(description):
    prefix = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: "
    response = client.images.generate(
        model="dall-e-3",
        prompt=prefix + description,
        size="1024x1792",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url

def download_image(image_url, filename):
    image_response = requests.get(image_url)
    image_response.raise_for_status()  # Raises an HTTPError for bad responses

    # Save the image to a file
    with open(filename, 'wb') as f:
        f.write(image_response.content)

    return filename

if __name__ == '__main__':
    title = "Do Androids Dream of Electric Sheep?"
    author = "Philip K Dick"

    book_info = get_book_info(author, title)
    book_info_json = json.dumps(book_info, indent=2)
    print(book_info_json)
    response = create_description(book_info_json)
    print(response)
    print("...")
    structured_response = json.loads(response.content)
    prompts = structured_response['prompts']
    for p in prompts:
        prompt = p['prompt']
        print("Prompt is "+prompt)
        image_url = generate_image(prompt)
        filename = p['theme']+".png"
        download_image(image_url, filename)

        title_font_path = structured_response['typeface']
        author_font_path = structured_response['typeface']
        light_color = structured_response['title_color'][0]
        dark_color = structured_response['title_color'][1]

        color = find_text_color(filename, light_color, dark_color)

        add_text_to_image(filename, title, author, title_font_path, author_font_path, color, color)
