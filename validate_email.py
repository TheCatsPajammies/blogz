def is_email_valid(email):
    
    is_valid=True

    for char in email:
        if char == '@':
            num_at += 1

        if char == '.':
            num_dot += 1

        if num_at > 1 or num_dot > 1:
            is_valid=False

        if char == ' ':
            is_valid=False

    if num_at != 1 and num_dot != 1:
        is_valid=False
    else:
        char_position = 0
        characters_since_at = 0
        at_exists = False
        characters_since_dot = 0
        dot_exists = False
        for i in email:
            if at_exists:
                characters_since_at += 1
            if dot_exists:
                characters_since_dot += 1
            if i == '@':
                at_exists = True
            if i == '.':
                dot_exists = True
            if dot_exists and at_exists:
                if characters_since_at < 2:
                    is_valid=False
            if i == '.' and char_position == len(email):
                is_valid=False
            char_position += 1
    
    return is_valid

if __name__ == "__main__":
    main()