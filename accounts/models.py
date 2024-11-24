from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

class UserProfile(models.Model):
    PROGRAMMING_LANGUAGES_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('csharp', 'C#'),
        ('cpp', 'C++'),
        ('ruby', 'Ruby'),
        ('go', 'Go'),
        ('php', 'PHP'),
        ('swift', 'Swift'),
        ('kotlin', 'Kotlin'),
        ('typescript', 'TypeScript'),
        ('scala', 'Scala'),
        ('rust', 'Rust'),
        ('dart', 'Dart'),
        ('objective_c', 'Objective-C'),
        ('perl', 'Perl'),
        ('haskell', 'Haskell'),
        ('lua', 'Lua'),
        ('r', 'R'),
        ('matlab', 'MATLAB'),
        ('groovy', 'Groovy'),
        ('vhdl', 'VHDL'),
        ('verilog', 'Verilog'),
        ('elixir', 'Elixir'),
        ('clojure', 'Clojure'),
        ('coffeescript', 'CoffeeScript'),
        ('fsharp', 'F#'),
        ('scheme', 'Scheme'),
        ('julia', 'Julia'),
        ('nim', 'Nim'),
        ('smalltalk', 'Smalltalk'),
        ('ada', 'Ada'),
        ('cobol', 'COBOL'),
        ('fortran', 'Fortran'),
        ('prolog', 'Prolog'),
        ('racket', 'Racket'),
        ('ocaml', 'OCaml'),
        ('tcl', 'Tcl'),
        ('assembly', 'Assembly'),
        ('bash', 'Bash'),
        ('powershell', 'PowerShell'),
        ('vba', 'VBA'),
        ('solidity', 'Solidity'),
        ('apl', 'APL'),
        ('awk', 'Awk'),
        ('d', 'D'),
        ('erlang', 'Erlang'),
        ('forth', 'Forth'),
        ('icon', 'Icon'),
        ('c', 'C'),
        ('sql', 'SQL'),
        ('visual_basic', 'Visual Basic'),
        ('delphi', 'Delphi/Object Pascal'),
        ('scratch', 'Scratch')
    ]

    SOCIAL_MEDIA_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('telegram', 'Telegram'),
        ('vk', 'VKontakte'),
        ('tiktok', 'TikTok'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    programming_languages = MultiSelectField(choices=PROGRAMMING_LANGUAGES_CHOICES, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default_avatar.jpg')

    # Социальные сети
    facebook = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.CharField(max_length=100, blank=True, null=True)
    youtube = models.CharField(max_length=100, blank=True, null=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    vk = models.CharField(max_length=100, blank=True, null=True)
    tiktok = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username