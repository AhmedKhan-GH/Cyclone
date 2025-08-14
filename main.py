# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import cyclone as cy

def main():
    print(cy.get_api_info())
    print(cy.get_package_info())
    print(cy.get_image_info("test_images/test.txt"))
    print(cy.get_image_info("test_images/BLANK.jpg"))
    print(cy.get_image_info("test_images/Empty.png"))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
