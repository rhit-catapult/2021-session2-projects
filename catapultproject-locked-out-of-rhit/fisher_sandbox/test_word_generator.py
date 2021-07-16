import word_utils

def main():
    word_generator = word_utils.WordGenerator()
    print("Testing with 3 words")
    letters, display_words = word_generator.generate_words(3)
    print(f"Letters: {letters}   Words: {display_words})")


    print("Testing with 12 words")
    letters, display_words = word_generator.generate_words(12)
    print(f"Letters: {letters}   Words: {display_words})")


main()