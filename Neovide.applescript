on replace_chars(this_text, search_string, replacement_string)
	set AppleScript's text item delimiters to the search_string
	set the item_list to every text item of this_text
	set AppleScript's text item delimiters to the replacement_string
	set this_text to the item_list as string
	set AppleScript's text item delimiters to ""
	return this_text
end replace_chars

on activate_open_instance(win_title, is_first_time)
	tell application "System Events"
		set neovideProcList to a reference to (every process whose name is "neovide")
		repeat with proc in neovideProcList
			set PID to proc's unix id
			set myFiles to paragraphs of (do shell script "lsof -F -p" & space & PID & space & "| grep ^n/ | cut -c2-")
			set fName to my replace_chars(win_title, "'", "")
			if myFiles contains fName then
				tell proc
					set frontmost to true
				end tell
				return true
			end if
		end repeat
	end tell
	
	return false
end activate_open_instance

on run {input, parameters}
	set enablePathVar to "eval \"$(/usr/libexec/path_helper -s)\"; PATH=$PATH:/opt/homebrew/bin neovide"
	try
		set filePath to quoted form of POSIX path of (input as text)
		if true or not my activate_open_instance(filePath, false) then
			set fileCmdPath to quoted form of (POSIX path of (input as text))
			do shell script enablePathVar & space & fileCmdPath
			delay 0.1
			my activate_open_instance(filePath, true)
		end if
	on error
		do shell script enablePathVar
	end try
	return input
end run