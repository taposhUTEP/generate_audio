from gtts import gTTS
import os

# The texts we wrote for you
scripts = {
    "1_Morning_Victory": """
        I am awake. The alarm is not a disturbance; it is an invitation to my future.
        I choose to rise. I choose to leave the comfort of these sheets because the comfort of success tastes sweeter. 
        I am not a person who negotiates with a clock. I am a person who commands it.
        Aristotle said, 'We are what we repeatedly do. Excellence, then, is not an act, but a habit.'
        Today, I choose the habit of excellence. I am up before the world is noisy. This is my time. 
        My mind is clear, my will is iron, and my potential is limitless. I am starting this day with a victory. 
        I am up. I am moving. I am alive.
    """,
    
    "2_Architect_of_Time": """
        I possess the same 24 hours as the greatest minds in history, and I use them with surgical precision. I do not drift; I direct.
        This PhD is not a burden I carry; it is a mountain I am conquering. Every sentence I write, every dataset I analyze, brings me closer to the summit. 
        I am capable of deep, profound focus. When I sit to work, the world disappears, and only my progress remains.
        I am judicious with my energy. I treat my time like gold. I do not spend it on worry; I invest it in action. 
        As Benjamin Franklin said, 'Energy and persistence conquer all things.'
        I have the energy. I have the persistence. I am finishing this degree strong. I am not just a student; I am an expert in the making.
    """,
    
    "3_Career_Warrior": """
        I am a powerhouse of skill and logic. When I look at the job market, I do not see scarcity; I see opportunity waiting for my specific talents.
        I am sharp. My mind is built for algorithms. When I review code, I see the patterns clearly. 
        When I solve problems, I am demonstrating the resilience I built during my PhD. 
        I am not 'studying' to catch up; I am polishing a weapon that is already dangerous.
        I approach my resume and applications with total confidence. I have value to offer. 
        I have solved hard problems before, and I will solve them for my future employer.
        Whatever company hires me is getting a massive asset. I walk into this phase of my life with my head high. 
        I am competent. I am prepared. I am ready to be hired.
    """,
    
    "4_All_Day_Loop": """
        I am the master of my attention span.
        I do not wait for motivation; I create it through action.
        My resume reflects a history of overcoming challenges.
        I love the challenge of a complex algorithm. I am a problem solver.
        I am upbeat, I am optimistic, and I am relentless.
        Every hour today is a brick in the castle of my future.
        I trust myself to get this done.
    """,
    
    "5_The_Reset": """
        Stop. Breathe.
        I am doing fine. I have handled everything life has thrown at me up to this point, and I will handle this too. 
        The stress I feel is just my ambition revving its engine.
        Winston Churchill said, 'If you're going through hell, keep going.'
        I am keeping going. I am taking the very next step. Just one line of code. Just one paragraph of the thesis. 
        Just one application. Motion cures fear. I am moving now.
    """
}

print("Generating audio files...")

for title, text in scripts.items():
    # clean up newlines for smoother reading
    clean_text = text.replace('\n', ' ').strip()
    
    tts = gTTS(text=clean_text, lang='en', slow=False)
    filename = f"{title}.mp3"
    tts.save(filename)
    print(f"Generated: {filename}")

print("Done! Check your folder for the MP3s.")

