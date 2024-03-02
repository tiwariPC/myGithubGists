## Use Automator app to create a workflow by selecting Folder Action.
## Then choose Downloads folder
## Add Run Shell Script option then add the script below to the box and save it in ~/Library/Workflows/Applications/Folder Actions/
## Then selection the folder action in Finder by double clicking the Download folder

for f in "$@"
do
	DEST=""
	LC_FILE=$(echo "$f" | tr '[:upper:]' '[:lower:]')  # Convert file to lowercase for case-insensitive checks
	
	if [[ $LC_FILE == *".pdf"* ]]
	then
		DEST="/Users/ptiwari/Downloads/Document"
	elif [[ $LC_FILE == *".doc"* ]] || [[ $LC_FILE == *".docx"* ]]
	then
		DEST="/Users/ptiwari/Downloads/DocFiles"
	elif [[ $LC_FILE == *".txt" ]] || [[ $LC_FILE == *".py" ]] || [[ $LC_FILE == *".c" ]] || [[ $LC_FILE == *".tex" ]] || [[ $LC_FILE == *".csv" ]] || [[ $LC_FILE == *".xml" ]]
	then
		DEST="/Users/ptiwari/Downloads/TextFiles"
    elif [[ $LC_FILE == *".key" ]] || [[ $LC_FILE == *".ppt"* ]] || [[ $LC_FILE == *".pptx"* ]]
	then
		DEST="/Users/ptiwari/Downloads/Presentations"
    elif [[ $LC_FILE == *".png" ]] || [[ $LC_FILE == *".jpg" ]] || [[ $LC_FILE == *".jpeg" ]] || [[ $LC_FILE == *".gif" ]] || [[ $LC_FILE == *".bmp" ]] || [[ $LC_FILE == *".tiff" ]] || [[ $LC_FILE == *".ico" ]] || [[ $LC_FILE == *".webp" ]] || [[ $LC_FILE == *".heic" ]]
	then
		DEST="/Users/ptiwari/Downloads/ImageFiles"
    elif [[ $LC_FILE == *".mov" ]] || [[ $LC_FILE == *".mp4"* ]] || [[ $LC_FILE == *".avi"* ]] || [[ $LC_FILE == *".mkv"* ]] || [[ $LC_FILE == *".wmv"* ]] || [[ $LC_FILE == *".flv"* ]] || [[ $LC_FILE == *".webm"* ]] || [[ $LC_FILE == *".m4v"* ]]
	then
		DEST="/Users/ptiwari/Downloads/VideoFiles"
	elif [[ $LC_FILE == *".zip" ]] || [[ $LC_FILE == *".tar"* ]] || [[ $LC_FILE == *".tar.gz"* ]] || [[ $LC_FILE == *".rar"* ]] || [[ $LC_FILE == *".7z"* ]] || [[ $LC_FILE == *".dmg"* ]] || [[ $LC_FILE == *".iso"* ]]
	then
		DEST="/Users/ptiwari/Downloads/Compressed"
	elif [[ $LC_FILE == *"/document/"* ]] || [[ $LC_FILE == *"/compressed/"* ]] || [[ $LC_FILE == *"/email/"* ]] || [[ $LC_FILE == *"/imagefiles/"* ]] || [[ $LC_FILE == *"/misc/"* ]] || [[ $LC_FILE == *"/miscellaneous/"* ]] || [[ $LC_FILE == *"/presentations/"* ]] || [[ $LC_FILE == *"/programs/"* ]] || [[ $LC_FILE == *"/skype/"* ]] || [[ $LC_FILE == *"/textfiles/"* ]] || [[ $LC_FILE == *"/video/"* ]] || [[ $LC_FILE == *"/videofiles/"* ]]
	then
		osascript -e "display notification \"$f Not Moved (Destination restricted).\""
	else
		DEST="/Users/ptiwari/Downloads/Miscellaneous"
	fi

	if [[ $DEST != "" ]]
	then
		mv "$f" "$DEST"
		# osascript -e "display notification \"Moved $f to $DEST\""
	fi
done
