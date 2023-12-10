import arcade
import arcade.gui

from views.view import View


class SelectView(View):
    def __init__(self):
        super().__init__()

        self.h_box_upper = None
        self.h_box_middle = None
        self.h_box_lower = None

        self.selected_player = None
        self.selected_difficulty = None

    def setup(self):
        super().setup()
        self.ui_manager = arcade.gui.UIManager()

        self.setup_buttons()

        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="top",
                align_y=-130,
                child=self.h_box_upper
            )
        )
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", 
                anchor_y="center", 
                align_y=-30,
                child=self.h_box_middle
            )
        )
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                align_y=100,
                child=self.h_box_lower,
            )
        )

    def setup_buttons(self):
        image_path = ':resources:images/animated_characters'
        self.h_box_upper = arcade.gui.UIBoxLayout(vertical=False)
        self.h_box_middle = arcade.gui.UIBoxLayout(vertical=False)
        self.h_box_lower = arcade.gui.UIBoxLayout(vertical=False)

        character_one_image = f'{image_path}/female_adventurer/female_adventurer_idle.png'
        character_one_texture = arcade.load_texture(character_one_image)
        character_one_button = arcade.gui.UITextureButton(
            texture=character_one_texture, width=96, height=128
        )
        @character_one_button.event("on_click")
        def on_click_character_one(event):
            self.selected_player = 'female_adventurer'
        self.h_box_upper.add(character_one_button.with_space_around(right=20))

        character_two_image = f'{image_path}/male_adventurer/male_adventurer_idle.png'
        character_two_texture = arcade.load_texture(character_two_image)
        character_two_button = arcade.gui.UITextureButton(
            texture=character_two_texture, width=96, height=128
        )
        @character_two_button.event("on_click")
        def on_click_character_two(event):
            self.selected_player = 'male_adventurer'
        self.h_box_upper.add(character_two_button.with_space_around(right=20))

        easy_button = arcade.gui.UIFlatButton(text="Easy", width=200, style={
            'font_color': arcade.color.BLACK,
            'bg_color': arcade.color.LIGHT_GREEN,
            'border_width': 2,
            'border_color': arcade.color.BLACK})
        @easy_button.event("on_click")
        def on_click_easy_button(event):
            self.selected_difficulty = 'easy'
        self.h_box_middle.add(easy_button.with_space_around(right=20))

        medium_button = arcade.gui.UIFlatButton(text="Medium", width=200, style={
            'font_color': arcade.color.BLACK,
            'bg_color': arcade.color.BLUE_BELL,
            'border_width': 2,
            'border_color': arcade.color.BLACK})
        @medium_button.event("on_click")
        def on_click_medium_button(event):
            self.selected_difficulty = 'medium'
        self.h_box_middle.add(medium_button.with_space_around(right=20))

        hard_button = arcade.gui.UIFlatButton(text="Hard", width=200, style={
            'font_color': arcade.color.BLACK,
            'bg_color': arcade.color.LIGHT_RED_OCHRE,
            'border_width': 2,
            'border_color': arcade.color.BLACK})
        @hard_button.event("on_click")
        def on_click_hard_button(event):
            self.selected_difficulty = 'hard'
        self.h_box_middle.add(hard_button.with_space_around(right=20))

        play_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        @play_button.event("on_click")
        def on_click_play(event):
            if self.selected_player and self.selected_difficulty:
                self.window.views['game'].selected_player = self.selected_player
                self.selected_player = None
                self.window.views['game'].difficulty = self.selected_difficulty
                self.selected_difficulty = None
                self.window.show_view(self.window.views['game'])
        self.h_box_lower.add(play_button.with_space_around(right=20))

        back_button = arcade.gui.UIFlatButton(text="Back", width=200)
        @back_button.event("on_click")
        def on_click_back(event):
            self.window.show_view(self.window.views['menu'])
        self.h_box_lower.add(back_button)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            'Select Character',
            self.window.width / 2,
            self.window.height - 100,
            arcade.color.BLACK,
            font_size=30,
            anchor_x='center',
            anchor_y='center',
        )
        arcade.draw_text(
            'Select Difficulty',
            self.window.width / 2,
            self.window.height - 336,
            arcade.color.BLACK,
            font_size=30,
            anchor_x='center',
            anchor_y='center',
        )
        arcade.draw_text(
            f"Selected Character: {self.selected_player}",
            self.window.width / 2,
            250,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
            italic=True
        )
        arcade.draw_text(
            f"Selected Difficulty: {self.selected_difficulty}",
            self.window.width / 2,
            220,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
            italic=True
        )

        self.ui_manager.draw()
