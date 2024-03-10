import g4f

def availableproviders():
    print([
    provider.__name__
    for provider in g4f.Provider.__providers__
        if provider.working
    ])

def askwithgpt(prompt):
    
    response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_35_turbo,
    provider=g4f.Provider.FlowGpt,
    messages=[{"role": "user", "content": prompt},
              ]
    )  # Alternative model setting
    return response
    
print(askwithgpt("Что ты можешь?"))
availableproviders()