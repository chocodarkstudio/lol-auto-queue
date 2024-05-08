
# League of Legends - Auto Queue Acceptor

Automatically accept queue, block, and select a champion
'*You can literally be pooping while waiting for a match, and the script will take care of the rest :)*'

## Requirements

- Python 3.6 or later
- `requests` library
- infi.systray
- PyAutoGUI
- PyGetWindow
- python-dotenv

## Installation

1. Clone this repository or download the files.
    ```bash
    git clone https://github.com/chocodarkstudio/lol-auto-queue.git
    cd lol-auto-queue
    ```

2. Install the required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

3. Edit the `config.json` file and replace `league_of_legends_path` with the actual path to your LoL game or `RiotClientServices.exe` directory.
    ```json
    "league_of_legends_path": "\"D:/Riot Games/Riot Client/RiotClientServices.exe\" --launch-product=league_of_legends --launch-patchline=live",
    ```

## Usage

1. Run the script:
    ```bash
    python lol_auto_queue.py
    ```

    > **You can also run it as a non-console program:**
    > rename the `lol_auto_queue.py` file to `lol_auto_queue.pyw` and use the built-in SysTrayIcon

2. Open the League of Legends client, you can use the systray shortcut or open it manually.

3. The script will periodically check if you are in a queue, and it will automatically accept the queue when a match is found.

4. It will automatically block and select your champion in `config.json` list.



## Compatibility

This script was tested on a screen resolution of 1366x768. You can find sample images for this resolution in the `imgs_1366x768` folder.

To ensure the script works for your setup, run a test queue match and observe if the script automatically accepts the queue and selects a champion. If it doesn't, you might need to take screenshots of the game buttons.

To add a new samples, follow these steps:
1.  **Take screenshots** of the relevant League of Legends buttons and create a new folder, similar to `imgs_1366x768`
1. **Edit the `settings.py` file** to add the new resolution to the list `availible_res`.
2. Set the index number for the script to use it.

Here is the `settings.py` section for reference:

```python
class Resolutions:
    availible_res = ["1366x768"]  # Add your new resolution here
    img_path = "imgs_" + availible_res[0]  # Set index to your desired resolution
```

## Contributing
If you'd like to contribute with new image samples for different screen resolutions or any other feature, feel free to submit a pull request or contact to me.