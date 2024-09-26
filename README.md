# Reddit Bot

## Overview

This Reddit Bot automates the process of interacting with Reddit communities. It logs in using credentials from a spreadsheet, searches for specified topics, and engages with posts and comments in relevant subreddits. The bot randomly upvotes posts and comments, simulating a natural browsing experience. Users can control the duration of scrolling and the intensity of interactions.

## Features

- **Automated Login**: Reads Reddit login credentials from a spreadsheet.
- **Custom Search**: Takes search terms from a spreadsheet and searches for relevant subreddits.
- **Random Upvoting**: Randomly upvotes posts and comments in various subreddits.
- **Scroll Time**: The bot scrolls for a user-defined time in each community, interacting with posts.
- **Adjustable Interaction Rate**: Modify the rate of upvoting posts using the "Posts to upvote" parameter.
- **Google Sheets Integration**: Customize the source spreadsheet by modifying the `sheet_id` in the `main` function of `Project.py`.
- **Multilogin Support**: The bot supports using Multilogin for browser automation (see Multilogin branch).

## How It Works

1. **Spreadsheet Input**: The bot reads Reddit login credentials and search keywords from a provided spreadsheet.
2. **Reddit Login**: The bot uses the credentials to log in to Reddit.
3. **Community Interaction**: Based on the search terms, the bot finds relevant subreddits, enters them, and scrolls through the feed.
4. **Upvoting Behavior**: 
   - The bot randomly upvotes posts as it scrolls through the feed.
   - Occasionally opens individual posts and randomly upvotes some comments.
5. **Parameter Control**: 
   - `Scroll Time`: Determines how long the bot will scroll in each community.
   - `Posts to upvote`: Controls the number of posts the bot interacts with during each scroll session.
   - **Port Number**: Only required when using Multilogin. If you're not using Multilogin, you can enter any random number for this parameter.

## Parameters

- **Scroll Time**: Time (in minutes) the bot will scroll through a subreddit.
- **Posts to upvote**: Number of posts the bot will randomly upvote during each scroll.
- **Port Number**: Used for Multilogin. Enter any random number if you're not using Multilogin.

## Google Sheets Integration

- You can modify the `sheet_id` in the `main` function of `Project.py` to use your own Google Sheets spreadsheet.
- Make sure to allow access to the sheet using the Google Sheets API.
- The Google Sheets API credentials should be stored in `credentials.py` in the same folder as other project files.

## Setup Instructions

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/yourusername/reddit-bot.git
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Provide your Reddit login credentials and search terms in the spreadsheet (follow the template in `credentials.xlsx`).

4. Modify the `sheet_id` in `Project.py` if you're using a custom Google Sheets file.

5. Enter a value for the `Port Number` parameter:
   - If using Multilogin, enter the correct port number.
   - If not using Multilogin, you can enter any random number.

6. Run the bot:
    ```bash
    python ui_project.py
    ```

7. If you wish to use Multilogin with this bot, please check out the [Multilogin branch](https://github.com/Simba256/reddit-bot/tree/Multilogin).

## Customization

You can adjust the `Scroll Time` and `Posts to upvote` parameters in the script or through command-line arguments, depending on your setup.

## Disclaimer

This bot is intended for educational and experimental purposes only. Please use responsibly and be mindful of Reddit’s [Terms of Service](https://www.redditinc.com/policies/data-api-terms).
