from textnode import TextType, TextNode


def main():
    dummy_textnode = TextNode("This is sample text: Lorem Ipsum", TextType.BOLD_TEXT)
    print(dummy_textnode)


if __name__ == "__main__":
    main()
