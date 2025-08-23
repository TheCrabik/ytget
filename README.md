# Ytget - a yt_dlp powered youtube downloader

## 1. Functions

- Flag system
- Video download
- File parsing and mass downloading. Possible to download from many different platforms at once (more about it in section 3)
- Build script

## 2. Flags and CLI usage

### 2.1. --help

Just typing in "ytget" will return an error.

```bash
[user@localhost ~]$ ytget
Error! No flags specified! Run with --help for basic documentation.
```

To get small documentation for basic usage run:

```bash
[user@localhost ~]$ ytget --help
```

It will return:

```bash
[user@localhost ~]$ ytget --help
Usage: ytget [OPTIONS] [URL]

Download youtube video/audio by providing some flags and URL or mass
download from file. More in readme.

Options:
  -g, --get [mp4|mkv|mp3|split]  Format choice: mp4 - MP4 (video+audio) mkv -
                                  MKV (video+audio) mp3 - MP3 (audio only)
                                  split - Both video and audio separately
  -p, --parse                    Executes parse module.
  --help                         Show this message and exit.
```

It is really basic documentation that does not contain anything about parsing. We'll get to it in section 3.

### 2.2. -g (--get)

Used to download individual videos. Usage:

```bash
[user@localhost ~]$ ytget -g mp4/mp3/mkv/split *(split downloads mp3 audio and mp4 video separately)* https://your/own/URL
```

This should return output like this if download successfully started:

```bash
Downloading from: https://www.youtube.com/watch?v=ExampleURL
Selected format: mp4
### Loading... ###
```

At the end of download it will give a filename and overall it will look like this:

```bash
Downloading from: https://www.youtube.com/watch?v=ExampleURL
Selected format: mp4
### Loading... ###
### Loading finished! ###
File saved as video21236407(It generates a random number)
[user@localhost ~]$ 
```

### 2.3. -p (--parse)

It is the most interesting option. It allows mass download from YouTube or even different platforms at once.

Used to parse url list from file:

```bash
[user@localhost ~]$ ytget -p
```

It will return this:

```bash
[user@localhost ~]$ ytget -p
Enter path to a file: 
```

You should enter path to a file where you want to parse from:

```bash
[user@localhost ~]$ ytget -p
Enter path to a file: /path/to/your/file
```

It will parse file for URLs. In section 3 are instructions on how to correctly set up file that should be parsed and more about parsing.

## 3. Parsing

### 3.1. Parsing errors

```bash
[user@localhost ~]$ ytget -p
Enter path to a file: /path/to/your/file
Parsing error!: File contains more than 2 strings
Parsing error has occured.
[user@localhost ~]$ 
```

This is an example of parsing error. In this case there are more than 2 strings in a file.

There are 2 kinds of parse errors:

1. **First kind**: As shown in the example above
2. **Second kind**: When it parses 'successfully' but inserts bad URLs

Example of the second kind:

```bash
Enter path to a file: /path/to/your/file
URL list:
1. https://example/url/1]https://example/url/2]https://example/url/3

Flags: mp4

Total URLs: 1

Processing URL 1/1: https://example/url/1]https://example/url/2]https://example/url/3
### Loading... ###
ERROR: [generic] Unable to download webpage: HTTP Error 404: Not Found (caused by <HTTPError 404: Not Found>)
Error during download: ERROR: [generic] Unable to download webpage: HTTP Error 404: Not Found (caused by <HTTPError 404: Not Found>)
[user@localhost ~]$ 
```

It happens if URL string (or flag string) is messed up.

### 3.2. Setting up a file

#### 3.2.1. Structure

```
URL string
(Optional) Flag string
```

#### 3.2.2. URL string

**Valid examples:**
- `https://example/url/1}https://example/url/2}https://example/url/3}https://...`
- `https://example/url/1 https://example/url/2 https://example/url/3 https://...`
- `{https://example/url/1}{https://example/url/2}{https://example/url/3}{https://...`

**Invalid examples:**
- `https://example/url/1]https://example/url/2]https://example/url/3]https://...`
- `https://example/url/1https://example/url/2https://example/url/3https://...`
- `[https://example/url/1][https://example/url/2][https://example/url/3][https://...`

#### 3.2.3. Flag string

This string contains format flag like you would use with -g flag: `mp4`, `mkv`, `mp3` or `split`.

Unknown flag will result in parsing error. No flag results in usage of default mp4 flag.

#### 3.2.4. File example

```txt
https://example/url/1}https://example/url/2}https://example/url/3}https://...
mp4
```

### 3.3. Successful parsing

Successful parsing will set up a line of URLs to get downloaded, like this:

```bash
Enter path to a file: /path/to/your/file
URL list:
1. https://example/url/1
2. https://example/url/2
3. https://example/url/3

Flags: mp4

Total URLs: 3

Processing URL 1/3: https://example/url/1
### Loading... ###
```

That's all about parsing.

## 4. Installation

This section is about how to actually install it.

### 4.1. Building using Build.sh

#### 4.1.1. Preparing

Before building you should install build dependencies:

```txt
yt_dlp, python-click, pyinstaller.
```

#### 4.1.2. Building

After that run:

```bash
[user@localhost ~]$ cd /dir/of/script
[user@localhost /dir/of/script]$ sudo ./Build.sh
```

#### 4.1.3. Notes

- pyinstaller should be installed in PATH!
- Make sure to run with bash, not in sh!
- You can choose to install it automatically or just compile binary instead.

### 4.2. Using precompiled binary

#### 4.2.1. Installing

Run this command:

```bash
[user@localhost ~]$ sudo cp "/dir/of/script/Compiled binary/ytget" /usr/local/bin
```

Now it is installed.

### 4.3. Using script itself

#### 4.3.1. Preparing

In case program is not starting from binary try this. Install dependencies:

```txt
yt_dlp, python-click.
```

Remove .py in ytget.py.

#### 4.3.2. Installing

Run this command:

```bash
[user@localhost ~]$ sudo chmod +x /dir/of/script/ytget
[user@localhost ~]$ sudo cp /dir/of/script/ytget /usr/local/bin
```

Now it is installed.

### 4.4. Notes

Build variant is recommended. Other variants are for a backup.

## 5. Troubleshooting

1. **Error! No flags specified! Run with --help for basic documentation.**
   - To fix this error you should specify a flag.

2. **Parsing error has occured.**
   - Look inside your file which you are parsing from and make sure that your URL and format string (if it exists) are following syntax.

3. **[download] Got error: HTTP Error 403: Forbidden**
   - It is a common yt-dlp issue. Try running `yt-dlp -U` or try downloading later.

4. **Why it discards some of parsed URLs?**
   - Check for `&start_radio` tag. Script throws away URLs with this tag.
   
## 6. For contributors

Thank's you for your interest in development!
All contributions are appreciated.
This section provides guidelines for developers, wanting to contribute.

### 6.1 Development setup

#### 6.1.1 Preparing

Make sure you have
- Python 3.7+
- pip (Python package manager)
- Git
- Click
- yt_dlp

#### 6.1.2 Setting up a development environment

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/ytget.git
cd ytget
```

2. **Install dependencies**

```txt
yt_dlp, Click, pyinstaller(recommended)
```

### 6.1.3 Project structure
```txt
/ytget/
|     /Compiled binary/
|-Build.sh            |-ytget
|-license.txt
|-ytget.py
|-ytget.spec
|-README.md
|-CHANGELOG.md
```
### 6.2 Testing

After implementing new features or fixes necessarily test them.

1. Run a script in your command line
```bash
[user@localhost /dir/of/script/]$ ytget.py
```
chmod +x if needed.

2. After testing build the script and see how binary behaves. Log all your fixes and implementations.

### 6.3 Adding New Features

Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```
Implement your changes
Add tests for your new functionality
Update documentation if needed
Submit a pull request with a clear description of changes

### 6.4 Release Process

Update version number in CHANGELOG.md
Update CHANGELOG.md
Run tests of script and of binary
Create a release tag
Update documentation if necessary.

### 6.5 Politeness rules

Please be respectful and inclusive when contributing and maintain a positive, collaborative environment. Dont leave innapropriate or offensive comments in code, documentation or changelog.

## 7. todo list

### This is list of features to be implemented
#### X means not done yet
#### ✓ means done
##### Current version of a project is only 0.8 so features are not here yet.

- Playlist download (-P, --playlist) - X
- Windows support - X
- Macos support - X 
- GUI branch - X
- More options - X
- String parsing (-Sp, --string-parse) - X
- More resolution options - X
- Customise quality options - X
- Deb, RPM, AUR packages - X
