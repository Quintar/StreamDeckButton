# Stream Deck Controller Button

This plugin is for the StreamController. It allows to set the 3 labels (top, center, bottom) to whatever text you send to localhost:65432 you just have to concatenate the string with a pipe "|" symbol (and end it for good measure)
Example: echo "Top|Centre|Bottom|" > /dev/tcp/localhost/65432

For more information checkout [the docs](https://streamcontroller.github.io/docs/latest/).
