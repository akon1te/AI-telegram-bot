
def get_start_text(name: str) -> str:
    return (f"Hello, {name}!\nI'm AI Painter bot! I can create picture for you!")

no_pics = (
    f"You didnt load any pictures!"
)

create_paths = (
    f"Choose how you want to create a photo.\n Can be photo -> photo, text -> photo, audio -> photo"
)

help_text = (
    "For generating pictures using Stable diffusion do this step by step:\n \
    Use command /create and after that write your text, send picture or voice message. (English language, pls!!!)\n \
    If you want to finish, send me /finish command."   
)

end_text = (
    f"Goodbye!)"
)