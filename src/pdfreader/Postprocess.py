"""
The script function is really long and confusing and unless you have additonal characters to take out or want to redo
the file please don't edit the code as it's easy to break but it works good with some tables so don't rely on it for tables

"""


# This is one is going one final time
def finalprocessing(string):
    i = 0
    special_characters = "!@#$%^&*()+?_=,<>/\"\'[];-_–"
    count = 0
    while i + 3 < len(string):

        # If there is a space and new line separating the characters joining them toghether because they are the same sentence
        if (string[i].isupper() or string[i].islower() or any(c in special_characters for c in string[i]) or string[
            i].isdigit()) \
                and string[i + 1] == " " and string[i + 2] == "\n" \
                and (string[i + 3].islower() or string[i + 3].isdigit()):
            string = string[:i + 1] + " " + string[i + 3:]
        if string[i] == "." and string[i + 1].isspace() and string[i + 2] == "\n" and string[i + 3].isupper():
            string = string[:i + 1] + " " + string[i + 3:]

        i += 1

    return string


def PostProcessing(string):
    print("Started Processing...")

    # There are some characters that the last character or the new line starts with and make them traated as a normal letter except a "."
    special_characters = "!@#$%^&*()+?_=,<>/\"\'[];-_–"

    # Removes the weird characters used to give more data in the table
    weird_characters = "†‡§"

    # Also replace the dash when the sentences uses a dash to indicate the space not enough and that the word continues on a new line
    string = string.replace("- ", "")

    # Dictionary switch for UTF-16 characters
    char_switch = {
        "ﬁ ": "fi",
        "": "ft",
        "ﬀ": "ff"
    }

    # Removing spaces after a new line to make the post-processing smooth
    string = string.replace("\n ", "\n")

    # While loop to take out the weird unicode character that indicates it's an image
    j = 0
    count = 1
    while j < len(string):
        if string[j] == "ð":
            string = string.replace("ð" + str(count) + "Þ", f"Image {str(count)}")
            count += 1
        j += 1

    # This is where the actual post-processing is done
    i = 0

    # Use a while to go through every character of the string that is passed to the function
    while i < len(string):
        '''if string[i] == "\n" and (string[i+1].islower() or string[i+1].isdigit()):
            string = string[:i] + " " + string[i+1:]
            #print("It worked")'''

        # Use the code below if your having spacing issues in the file
        # string = string.replace("\n ", "\n")

        # Incase the line stops at a comma and continues on a new line
        if string[i] == "," and string[i + 2] == "\n":
            string = string[:i] + " " + string[i + 1:]

        # Unless you are going to do it please don't mess up the order
        if (i + 2) < len(string):

            # When the last character is a space and before is a character that is not a full stop it join the sentences
            if (string[i].islower() or string[i].isdigit() or any(c in special_characters for c in string[i])) \
                    and string[i + 1] == " " and string[i + 2] == "\n": \
                    # and (string[i+3].islower() or string[i+3].isdigit() or string[i+3].isupper() or any(c in weird_characters for c in string[i+3])):
                string = string[:i + 1] + " " + string[i + 3:]

            # When the first character is a special character and last letter of the previous sentence is not a full stop
            if (string[i].isprintable() and string[i] == ".") and string[i + 1] == "\n" \
                    and any(c in special_characters for c in string[i + 2]):
                string = string[:i + 1] + string[i + 2:]

            # Removes the extra new lines for the fotters of tables
            if any(c in weird_characters for c in string[i]) and string[i + 1] == "\n" and string[i + 2].isdigit():
                string = string[:i + 1] + " " + string[i + 2:]

            # Same thing as above but in reverse order and also includes lower letter
            if (string[i].islower() or string[i].isdigit()) and string[i + 1] == "\n" and any(
                    c in special_characters for c in string[i + 2]):
                string = string[:i + 1] + " " + string[i + 2:]

            # Incase there is a new line between a digit and a lower letter
            if string[i].isdigit() and string[i + 1] == "\n" and (string[i + 2].islower() or string[i + 2].isdigit()):
                string = string[:i] + " " + string[i + 2:]

            # Removing a new line in between a special character and a lower character or a number
            if any(c in special_characters for c in string[i]) and string[i + 1] == "\n" and (
                    string[i + 2].islower() or string[i + 2].isdigit()):
                string = string[:i + 1] + " " + string[i + 2:]

            # Remove the new line if it's between a letter and digit
            if (string[i].islower() or string[i].isupper()) and string[i + 1] == "\n" and string[i + 2].isdigit():
                string = string[:i + 1] + string[i + 2:]

            # Remove the - and new line that used to indicate the word continues on a new line
            if string[i] == "-" and string[i + 1] == "\n":
                string = string[:i] + string[i + 2:]

            # kind of the same as the before the upper one but detailed to incorporate more
            if (string[i].islower() or string[i].isupper()) and string[i + 1] == "\n" \
                    and (string[i + 2].islower() or string[i + 2].isupper() or any(
                c in special_characters for c in string[i + 2]) or string[i + 2].isspace()):
                string = string[:i + 1] + " " + string[i + 2:]
        i += 1

    # Used a dictionary to replace unwanted or UTF-16 characters to UTF8 characters
    for word, replacement in char_switch.items():
        string = string.replace(word, replacement)

    # Final replacement of double spaces and spaces with a dash of compound names
    string = string.replace("  ", " ")
    string = string.replace("- ", "-")
    string = string.replace("\n)", ")")

    finalString = finalprocessing(string)

    return finalString

def fitzPostProcess(string):
    string = str(string)
    string = string.replace("-\n", "")
    i = 0
    while i+2 < len(string):
        if string[i].isspace() and string[i+1] == "\n" and string[i+2].isprintable():
            string = string[:i+1] + string[i+2:]


        i += 1

    return string