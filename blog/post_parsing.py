def html_parse(post_text, max_length=0):
    """Returns the HTML parsed from a post's text."""
    ### Note that "length" of a post is arbitrary -- it could be words, paragraphs, images, etc. -- its definition may change ###
    cur_length = 0
    html = ''
    in_paragraph = False
    for i in xrange(len(post_text)):
        if max_length > 0 and cur_length >= max_length:
            break
        if post_text[i] != '\n':
            if not in_paragraph:
                in_paragraph = True
                html += '<p>'
            html += post_text[i]
        else:
            in_paragraph = False
            html += '</p>'
            cur_length += 1
    return html
