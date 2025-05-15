# code for Ecommerce generators exclusively
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os
import shutil
import webbrowser
import pprint
import re

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
# chains them together using langchain
chain = prompt | model

def load_template(file_path):
    """Read the HTML template from a file with UTF-8 encoding."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def satisfaction(context, result):
    ans = input("are you satisfied with this response if yes enter 'yes' else 'no': ")
    if ans.lower() == "no":
        while 1:
            user_input = "Give me a better answer just the text alone no need to type anything like 'Here's a 40-word extract:' or 'Here's a 15-word extract:'"
            result = chain.invoke({"context": context, "question": user_input})
            print("Bot: ", result)
            ans_again = input("If satisfied enter 1 else 2: ")
            if ans_again == "1":
                break
            else:
                continue
    elif ans.lower() != "Yes" or ans == "Yes":
        print("Great!")
    return result

def ai_helper(business_type,section):
    context=""
    if section == "1":
        user_input = f"write a 15 word short intro about my business which is a {business_type} without including names or anything such as [your name] no need to type anything like 'Here's a 40-word extract:"
        result = chain.invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"
        return satisfaction(context, result)
    if section == "2":
        user_input = f"ok can you give me a 40 word extract going into detail about why you should choose my business which is a {business_type} no need to type anything like 'Here's a 40-word extract:'"
        result = chain.invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"
        return satisfaction(context, result)


def business_info_getter(business_type):
    name = input("Enter the name of your business: ")
    ai_ans = input("Do you want to use AI to generate a short intro? (y/n): ").lower()

    if ai_ans == "y":
        print("The AI is generating text for you")

        if business_type == "cafe":
            intro1 = ai_helper("Cafe", "1")
            print("The AI is generating more text for you")
            about_me_info = ai_helper("Cafe", "2")
        elif business_type == "gym":
            intro1 = ai_helper("GYM", "1")
            print("The AI is generating more text for you")
            about_me_info = ai_helper("GYM", "2")
        elif business_type == "Jewelry Store":
            intro1 = ai_helper("Jewelry Store", "1")
            print("The ai is generating more text for you")
            about_me_info = ai_helper("Jewelry Store", "2")
    else:
        intro1 = input("Enter a short intro about your business: ")
        about_me_info = input("Enter a detailed description of your business: ")
    
    history = input("Enter a brief history of your business: ")
    email = input("Enter the business' email: ")
    phone = input("Enter the business' phone number: ")
    address = input("Enter the business' address: ")
    pfp = input("Enter the path to a picture for your about Screen: ").strip('"')

    reviews = []
    for i in range(3):  
        review = input(f"Enter review {i + 1} of your business: ")
        reviews.append(review)

    ecommerce_info = {
        "name": name,
        "intro1": intro1,
        "about_me_info": about_me_info,
        "history": history,
        "pfp": pfp,
        "reviews": reviews,
        "contact": {
            "email": email,
            "phone": phone,
            "address": address
        }
    }
    return ecommerce_info

def cafe_info_getter():
    products = []
    num_products = int(input("Enter the number of products you want to add: "))
    for i in range(num_products):
        product = input(f"Enter product {i + 1}: ")
        products.append(product)
    product_images = []
    print("Enter", num_products, " file path to images for your products")
    for i in range (num_products):
        image = input("Enter the path to your product picture: ").strip('"')
        product_images.append(image)
    # pfp = input("Enter the path to a picture for your about Screen: ").strip('"')
    home1 = input("Enter the path to a picture for your Home Screen: ").strip('"')

    ecommerce_info = {
        "products": products,
        "images": product_images,
        "home1":home1
    }

    return ecommerce_info

def gym_info_getter():
    services = {}
    plans = {}

    print("Enter information for 6 gym services:")

    for i in range(1, 7):
        service_name = input(f"Enter name for service {i}: ").strip()
        service_img = input(f"Enter image filename (or path) for service {i}: ").strip('"')

        # Store values in the dictionary with the correct keys
        services[f"service{i}"] = service_name
        services[f"service_img{i}"] = service_img

    about_image = input("Enter the image path for the About section: ").strip('"')
    services["about_us_img"] = about_image

    print("Enter information for 3 gym pricing plans:\n")


    for i in range(1, 4):
        plan_name = input(f"Enter name for plan {i}: ").strip()
        plan_price = input(f"Enter price for plan {i}: ").strip()

        plans[f"plan{i}"] = plan_name
        plans[f"price{i}"] = plan_price

    print("\nNow enter the features for each plan:")

    # Features 1–2 for plan 1
    for i in range(1, 3):
        plans[f"feature{i}"] = input(f"Enter feature {i} for Plan 1: ").strip()

    # Features 3–5 for plan 2
    for i in range(3, 6):
        plans[f"feature{i}"] = input(f"Enter feature {i} for Plan 2: ").strip()

    # Features 6–9 for plan 3
    for i in range(6, 10):
        plans[f"feature{i}"] = input(f"Enter feature {i} for Plan 3: ").strip()

    return {**services, **plans}

def jewelry_info_getter():
    jewelry_data = {}

    print("Enter information for 3 different jewelry products:\n")

    for i in range(1, 4):
        # Prompt for the jewelry title and image
        name = input(f"Enter name/title for Jewelry {i}: ").strip()
        image = input(f"Enter image filename or path for Jewelry {i}: ").strip('"')

        # Store the data in the dictionary
        jewelry_data[f"jewelry{i}"] = name
        jewelry_data[f"jewelry_img{i}"] = image
    
    new_product_data = {}

    print("Enter information for 7 different jewelry products:\n")

    for i in range(4, 11):  # Jewelry 4 to 10
        name = input(f"Enter name/title for Jewelry {i}: ").strip()
        image = input(f"Enter image filename or path for Jewelry {i}: ").strip('"')
        price = input(f"Enter price for Jewelry {i}: ").strip()

        new_product_data[f"jewelry{i}_text"] = name
        new_product_data[f"jewelry_img{i}"] = image
        new_product_data[f"price{i - 3}"] = price  # price1 to price7

    
    category_data = {}

    print("Enter information for 4 different categories:\n")

    output_image_folder = "User_Ecommerce"  # Folder where HTML and images go

    for i in range(1, 5):
        name = input(f"Enter name/title for Category {i}: ").strip()
        image_path = input(f"Enter image filename or path for Category {i}: ").strip('"')

        # Copy image to output folder
        image_filename = os.path.basename(image_path)
        destination_path = os.path.join(output_image_folder, image_filename)

        try:
            shutil.copy(image_path, destination_path)
            print(f"✅ Copied {image_filename} to {output_image_folder}")
        except FileNotFoundError:
            print(f"❌ File not found: {image_path}")
        except Exception as e:
            print(f"⚠️ Error copying {image_filename}: {e}")

        # Store relative path (just the filename)
        category_data[f"category_name{i}"] = name
        category_data[f"category_img{i}"] = image_filename
    
    feature_data = {}
    output_image_folder = "User_Ecommerce"  # Make sure this folder exists

    print("Enter information for 5 featured products:\n")

    for i in range(1, 6):  # Asking for 5 featured products
        name = input(f"Enter name/title for Feature Product {i}: ").strip()
        image_path = input(f"Enter image filename or path for Feature Product {i}: ").strip('"')
        price = input(f"Enter price for Feature Product {i}: ").strip()

        # Extract just the filename from the path
        image_filename = os.path.basename(image_path)

        # Copy image to the destination folder
        try:
            shutil.copy(image_path, os.path.join(output_image_folder, image_filename))
            print(f"✅ Copied {image_filename} to {output_image_folder}")
        except Exception as e:
            print(f"⚠️ Failed to copy {image_path}: {e}")

        # Store relative filename in the dictionary
        feature_data[f"feature_name{i}"] = name
        feature_data[f"feature_img{i}"] = image_filename
        feature_data[f"feature_price{i}"] = price
    
    # Combine all dictionaries into one
    combined_data = {}
    combined_data.update(jewelry_data)
    combined_data.update(new_product_data)
    combined_data.update(category_data)
    combined_data.update(feature_data)

    return combined_data


def ecommerce_type():
    destination_folder = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\User_Ecommerce"
    print("Enter the portfolio of your choosing by entering the corresponding number")
    choice = input("1.Cafe Website\n2.Gym Website\n3.Jewelry Website\n")
    match choice:
        case "1":
            print("A Cafe nice and Cozy")
            info = business_info_getter("cafe")
            cafe_info = cafe_info_getter()
            
            # Manually merge to preserve nested 'contact' dictionary
            combined_info = info.copy()
            for key, value in cafe_info.items():
                if key in combined_info and isinstance(combined_info[key], dict) and isinstance(value, dict):
                    combined_info[key].update(value)
                else:
                    combined_info[key] = value

            print(combined_info)  # Optional, to check the merged dictionary structure

            # Define the source and destination paths
            source_path = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Ecommerce_templates\Cafestyle.css"
            # Copy the file
            shutil.copy(source_path, destination_folder)

            js_path = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Ecommerce_templates\Cafescript.js"
            shutil.copy(js_path, destination_folder)
            
            template = load_template("Ecommerce_templates\Cafeindex.html")
            
            # Proceed with template and generator call
            generator(combined_info, template, "Cafe")
        
        case "2":
            print("A Gym to get fit and healthy")
            info = business_info_getter("gym")
            gym_info = gym_info_getter()

            combined_data = {**info, **gym_info}
            
            # print("\nCombined Data:")
            # pprint.pprint(combined_data)
            print(combined_data)

            source_path = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Ecommerce_templates\Gymstyle.css"
            shutil.copy(source_path, destination_folder)
            
            js_path = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Ecommerce_templates\Gymscript.js"
            shutil.copy(js_path, destination_folder)

            template = load_template("Ecommerce_templates\GymIndex.html")
            generator(combined_data, template, "Gym")
        
        case "3":
            print("Jewelry very fancy")
            info = business_info_getter("Jewelry Store")
            jewelry_info = jewelry_info_getter()

            combined_data = {**info, **jewelry_info}
            # print("\nCombined Data:")
            # pprint.pprint(combined_data)
            print(combined_data)

            source_path = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Ecommerce_templates\Jewerlystyle.css"
            shutil.copy(source_path, destination_folder)

            template = load_template("Ecommerce_templates\Jewerlyindex.html")
            generator(combined_data, template, "Jewelry")
            

        case _:
            print("Invalid choice")
            return ecommerce_type()
        
def generator(info, template, business):
    # Move the image to the project folder
    destination_folder = "User_Ecommerce"
    os.makedirs(destination_folder, exist_ok=True)

    # Copy the image to the destination folder
    destination_path = os.path.join(destination_folder, os.path.basename(info["pfp"]))
    shutil.copy(info["pfp"], destination_path)
    
    # Set the relative path for the HTML
    pfp_path = f"{os.path.basename(info['pfp'])}"

    if business == "Cafe":
        destination_path2 = os.path.join(destination_folder, os.path.basename(info["home1"]))
        shutil.copy(info["home1"], destination_path2)

        home1_path = f"{os.path.basename(info['home1'])}"
        # Retrieve product names and images
        products = info["products"]
        images = info["images"]



        # Copy product images and generate dynamic product boxes
        product_boxes = ""
        for i, (product, image) in enumerate(zip(products, images)):
            image_filename = os.path.basename(image)
            image_destination = os.path.join(destination_folder, image_filename)
            
            if os.path.exists(image):
                shutil.copy(image, image_destination)
            else:
                print(f"Error: Image {image} not found. Using placeholder.")
                image_filename = "default.jpg"

            product_boxes += f'''
                <div class="box">
                    <!-- editable: product_img{i} -->
                    <img src="{image_filename}" alt="{product}">
                    <!-- endeditable -->
                    <h3><!-- editable: product{i} -->{product}<!-- endeditable --></h3>
                    <div class="content">
                        <span><!-- editable: product_price{i} -->$25<!-- endeditable --></span>
                        <a href="#">Add to cart</a>
                    </div>
                </div>
            '''



        # Update the template with dynamic products
        
        page = template.format(name=info["name"],
                intro1=info["intro1"],
                about_me_info=info["about_me_info"],
                history=info["history"],
                address=info["contact"]["address"],
                phone=info["contact"]["phone"],
                email=info["contact"]["email"],
                review1=info["reviews"][0],
                review2=info["reviews"][1],
                review3=info["reviews"][2],
                pfp=pfp_path,
                home1 = home1_path,
                products=product_boxes
        )

    elif business == "Gym":
        # Flatten nested data like contact.email
        flat_data = flatten_dict(info)

        # Set relative path
        flat_data["pfp"] = os.path.basename(info["pfp"])

        # Manually add review placeholders
        flat_data["review1"] = info["reviews"][0] if "reviews" in info and len(info["reviews"]) > 0 else ""
        flat_data["review2"] = info["reviews"][1] if "reviews" in info and len(info["reviews"]) > 1 else ""
        flat_data["review3"] = info["reviews"][2] if "reviews" in info and len(info["reviews"]) > 2 else ""

        # Replace placeholders in template
        for key, value in flat_data.items():
            placeholder = f"{{{key}}}"
            template = template.replace(placeholder, str(value))

        # Store the final HTML
        page = template

    elif business == "Jewelry":
        # Flatten nested data if necessary (like category names, images, etc.)
        flat_data = info  # Assuming combined_data doesn't have deep nesting.

        # Set relative paths for images (if needed)
        flat_data["category_img1"] = os.path.basename(info["category_img1"])
        flat_data["category_img2"] = os.path.basename(info["category_img2"])
        flat_data["category_img3"] = os.path.basename(info["category_img3"])
        flat_data["category_img4"] = os.path.basename(info["category_img4"])

        flat_data["feature_img1"] = os.path.basename(info["feature_img1"])
        flat_data["feature_img2"] = os.path.basename(info["feature_img2"])
        flat_data["feature_img3"] = os.path.basename(info["feature_img3"])
        flat_data["feature_img4"] = os.path.basename(info["feature_img4"])
        flat_data["feature_img5"] = os.path.basename(info["feature_img5"])

        # Manually add any other placeholders (prices, titles, etc.)
        flat_data["feature_name1"] = info["feature_name1"]
        flat_data["feature_name2"] = info["feature_name2"]
        flat_data["feature_name3"] = info["feature_name3"]
        flat_data["feature_name4"] = info["feature_name4"]
        flat_data["feature_name5"] = info["feature_name5"]

        flat_data["feature_price1"] = info["feature_price1"]
        flat_data["feature_price2"] = info["feature_price2"]
        flat_data["feature_price3"] = info["feature_price3"]
        flat_data["feature_price4"] = info["feature_price4"]
        flat_data["feature_price5"] = info["feature_price5"]

        flat_data["category_name1"] = info["category_name1"]
        flat_data["category_name2"] = info["category_name2"]
        flat_data["category_name3"] = info["category_name3"]
        flat_data["category_name4"] = info["category_name4"]

        # Reviews - manually add review placeholders
        flat_data["review1"] = info["reviews"][0] if "reviews" in info and len(info["reviews"]) > 0 else ""
        flat_data["review2"] = info["reviews"][1] if "reviews" in info and len(info["reviews"]) > 1 else ""
        flat_data["review3"] = info["reviews"][2] if "reviews" in info and len(info["reviews"]) > 2 else ""

        # Replace placeholders in the template with the data from combined_data
        for key, value in flat_data.items():
            placeholder = f"{{{key}}}"
            template = template.replace(placeholder, str(value))

        # Store the final HTML
        page = template
        
    # Define the file path
    file_name = input("Enter the name of the file (do not enter '.html'): ")
    file_path = os.path.join(destination_folder, file_name + ".html")

    # Create and write the HTML file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(page)

    # Open the HTML file in the default browser
    webbrowser.open(f"file://{os.path.abspath(file_path)}")
    
def flatten_dict(d, parent_key='', sep='.'):
    """Flattens a nested dictionary into dot-separated keys for template replacement."""
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

if __name__ == "__main__":
    ecommerce_type()

    # cafe_dict = {'name': 'Galaxy', 'intro1': 'Cozy neighborhood spot serving artisanal coffee, fresh pastries, and warm hospitality since morning till evening.', 'about_me_info': '"Step into our cozy cafe and experience exceptional service, expertly crafted coffee drinks, and mouthwatering pastries. Our warm atmosphere and attentive staff make every visit feel like a treat. Come for the food, stay for the friendliness - your new favorite spot awaits!"', 'history': 'Something', 'pfp': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\jinx.jpg', 'reviews': ['Awesome', 'Awesome', 'Awesome'], 'contact': {'email': 'something', 'phone': '23456789', 'address': 'something'}, 'products': ['Hot Chocolate', 'French Vanilla', '33'], 'images': ['C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\hotChocolate.jpg', 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\french_vanilla.jpg', 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\33.jpg'], 'home1': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\viktor.jpg'}
    # cafe_template = load_template("Ecommerce_templates\Cafeindex.html")
    # business = "Cafe"

    # generator(cafe_dict, cafe_template, business)

    # gym_dict = {'name': 'Basic', 'intro1': '"Empowering individuals to reach their fitness goals, one sweat-filled workout at a time."', 'about_me_info': '"Join our gym and experience unparalleled fitness results! Our expert trainers, state-of-the-art equipment, and supportive community propel you towards achieving your goals. Personalized attention, small class sizes, and flexible scheduling ensure a tailored fit for every lifestyle."', 'history': 'Something', 'pfp': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\americano.jpg', 'reviews': ['Awesome', 'Awesome', 'Awesome'], 'contact': {'email': 'Something', 'phone': 'Something', 'address': 'Something'}, 'service1': 'Basic', 'service_img1': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\james.jpg', 'service2': 'Basic', 'service_img2': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\james.jpg', 'service3': 'Basic', 'service_img3': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\james.jpg', 'service4': 'Basic', 'service_img4': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\james.jpg', 'service5': 'Basic', 'service_img5': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\james.jpg', 'service6': 'Basic', 'service_img6': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\james.jpg', 'about_us_img': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\d6c4bf6d57d9e20df7ee967c9754e5e2.jpg', 'plan1': 'Basic', 'price1': '50/month', 'plan2': 'Basicer', 'price2': '500/month', 'plan3': 'Basicest', 'price3': '5000/month', 'feature1': 'Basic', 'feature2': 'Basic', 'feature3': 'Basic', 'feature4': 'Basic', 'feature5': 'Basic', 'feature6': 'Basic', 'feature7': 'Basic', 'feature8': 'Basic', 'feature9': 'Basic'}
    # gym_template = load_template("Ecommerce_templates\GymIndex.html")
    # business = "Gym"

    # generator(gym_dict, gym_template, business)

    # jewelry_dict = {'name': 'Basic', 'intro1': 'Sparkling treasures await at our enchanting jewelry store, where elegance meets timeless style and beauty.', 'about_me_info': '"Step into a world of sparkling treasures at our jewelry store! With unparalleled customer service, expert appraisals, and an extensive collection of unique pieces, we\'ll help you find the perfect symbol of love, celebration, or self-expression. Come discover why we\'re the go-to destination for discerning jewelers."', 'history': 'Something', 'pfp': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\Korvo.jpg', 'reviews': ['Awesome', 'Awesome', 'Awesome'], 'contact': {'email': 'Something', 'phone': 'Something', 'address': 'Something'}, 'jewelry1': 'Rings', 'jewelry_img1': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\jinx.jpg', 'jewelry2': 'Bracelets', 'jewelry_img2': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\Emily.jpg', 'jewelry3': 'Necklaces', 'jewelry_img3': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\daud.jpg', 'jewelry4_text': 'Ring', 'jewelry_img4': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\33.jpg', 'price1': '$50', 'jewelry5_text': 'Ring', 'jewelry_img5': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\33.jpg', 'price2': '$50', 'jewelry6_text': 'Ring', 'jewelry_img6': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\33.jpg', 'price3': '$50', 'jewelry7_text': 'Ring', 'jewelry_img7': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\33.jpg', 'price4': '$50', 'jewelry8_text': 'Ring', 'jewelry_img8': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\33.jpg', 'price5': '$50', 'jewelry9_text': 'Ring', 'jewelry_img9': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\33.jpg', 'price6': '$50', 'jewelry10_text': 'Ring', 'jewelry_img10': 'C:\\Users\\nites\\OneDrive\\Desktop\\desktop stuff 2\\wallpaper\\33.jpg', 'price7': '$50', 'category_name1': 'Rings', 'category_img1': '33.jpg', 'category_name2': 'Bracelets', 'category_img2': 'daud.jpg', 'category_name3': 'Necklaces', 'category_img3': 'Emily.jpg', 'category_name4': 'Earrings', 'category_img4': 'jinx.jpg', 'feature_name1': 'Rings', 'feature_img1': 'james.jpg', 'feature_price1': '30', 'feature_name2': 'Rings', 'feature_img2': 'james.jpg', 'feature_price2': '30', 'feature_name3': 'Rings', 'feature_img3': 'james.jpg', 'feature_price3': '30', 'feature_name4': 'Rings', 'feature_img4': 'james.jpg', 'feature_price4': '30', 'feature_name5': 'Rings', 'feature_img5': 'james.jpg', 'feature_price5': '30'}
    # jewelry_template = load_template("Ecommerce_templates\Jewerlyindex.html")
    # business = "Jewelry"
    
    # generator(jewelry_dict, jewelry_template, business)

