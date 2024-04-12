from utils import generate_pages_recursive


def main():
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
