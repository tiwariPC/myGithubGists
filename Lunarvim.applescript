-- make application in automator and then choose option Run Applescript and paste the following code, save as Lunarvim.app
on run {input, parameters}
	set randomChar to ASCII character (random number from 97 to 122)
	try
		set filename to ""
		repeat with i from 1 to length of input
			set cur to item i of input
			set filename to filename & " " & quote & POSIX path of cur & quote
		end repeat
	on error
		set filename to "untitled" & randomChar & ".txt"
	end try
	set cmd to "clear;cd `dirname " & filename & "`;/Users/ptiwari/.local/bin/lvim " & filename
	tell application "iTerm"
		set created to false
		if not (exists current window) then
			create tab with profile "Default"
			set created to true
		end if
		tell current window
			if not created then
				create tab with profile "Default"
			end if
			tell current session
				activate
				write text cmd
			end tell
		end tell
	end tell
end run