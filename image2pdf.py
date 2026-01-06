from PIL import Image
import os

def images_to_pdf(image_folder, output_pdf):
    images = []

    for file in sorted(os.listdir(image_folder)):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(image_folder, file)
            img = Image.open(img_path).convert('RGB')
            images.append(img)

    if not images:
        print("No images found!")
        return

    images[0].save(
        output_pdf,
        save_all=True,
        append_images=images[1:]
    )

    print(f"PDF created successfully: {output_pdf}")

# Example usage
images_to_pdf("images", "output.pdf")
