def read_prompts_from_file(filename):    
    """
    Read the content of the fiile (particularly prompt in our project)
    """
    try:     
        txt_file = open(filename, 'r', encoding='utf-8')    
        prompts = []

        for line in txt_file:
            prompt = line.replace('\n', '')        
            prompts.append(prompt)

        return prompts
    
    except FileNotFoundError:
        raise Exception(f'{filename} does not exist')
