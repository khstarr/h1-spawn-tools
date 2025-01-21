@echo off


:welcome
REM - Welcome Message
echo.
echo ::: WELCOME!
echo ::: Halo Batch Injector
echo ::: Version 0.9.2 - written by insidi0us
echo.
echo     IMPORTANT NOTES:
echo      _____
echo     /     \   1. When typing directories, use\back\slashes between folders.
echo     \     /   2. Do NOT include a slash at the end.
echo      \   /    3. This script will NOT modify the selected .scenario file.
echo       \_/        - A copy will be made, with a unix timestamp appended.
echo        _      4. It's still a good idea to make backups before starting.
echo       ^(_^)   5. This batch is not a natural formation. Someone built it. 
echo.



setlocal enabledelayedexpansion

echo.
:set_tags_folder
REM - Get tags folder from user
set "tags_folder=tags"
echo To set your tags folder to "tags", press [Enter]
set /p tags_input= or manually type your tags folder name: 
REM set /p tags_input= Input your tags folder, or press [Enter] to use "tags": 
if not "%tags_input%"=="" set "tags_folder=%tags_input%"
if not exist %tags_folder% (
	echo      _
	echo     ^| ^|   Whoops^^!
	echo     ^|_^|   The folder "%tags_input%" was not found. Please verify that this .bat file is 
	echo      _    in the same directory as your tags folder, or double check the spelling
	echo     ^(_^)   and try again...
	echo.
	set "tags_input="
	goto set_tags_folder
)

echo.
:set_maps_folder
REM - Get maps folder from user
set "maps_path=levels\test"
echo To set your maps folder to "%tags_folder%\levels\test", press [Enter]
set /p maps_input= or for non-standard setups, complete the path after %tags_folder%\
if not "%maps_input%"=="" set "maps_path=%maps_input%"
if not exist %tags_folder%\%maps_path% (
	echo      _
	echo     ^| ^|   Whoops^^!
	echo     ^|_^|   Folder not found. Please verify format and spelling: 
	echo      _    %tags_folder%\path\to\folder_containing_map_folders
	echo     ^(_^)   and try again...
	echo.
	set "maps_input="
	goto set_maps_folder
)
echo.

set "map_message=Select map folder by number, then press [Enter]: "
:select_map
REM - Get map folder from user
set /A n=0
echo.
echo Looking for map folders in %tags_folder%\%maps_path%...
echo.
for /f "usebackq tokens=*" %%a in (`dir /b %tags_folder%\%maps_path%`) do (
REM for /f "usebackq tokens=*" %%a in (`dir /b tags\levels\test`) do (
    echo: !n!: %%~nxa
	set folders[!n!]=%%~nxa
	set /A n+=1
)
echo.
set /p maps_input= !map_message!

REM - Check if map input is a valid number
set /a test_maps_input=maps_input
if !test_maps_input! EQU 0 (
	if !maps_input! EQU 0 (
		goto valid_map
	) else (
		goto invalid_map
	)
) else (
	REM - The variable n is increased one extra time after the last map folder is found,
	REM   so we need to check that the input is greater than or equal to 0, and less than n
	if !maps_input! GEQ 0 (
		if !maps_input! LSS !n! (
			goto valid_map
		) else (
			goto invalid_map
		)
	) else (
		goto invalid_map
	)
)

:invalid_map
set "map_message=You did not enter a valid map number. Please try again: "
goto select_map

:valid_map
set "map=!folders[%maps_input%]!"


set "scenario_message=Select scenario file by number, then press [Enter]: "
:select_scenario
REM - Get scenario file from user
set /A s=0
echo.
echo Looking for scenario files in %tags_folder%\%maps_path%\%map%...
echo.
for /f "usebackq tokens=*" %%a in (`dir /b %tags_folder%\%maps_path%\%map%`) do (
	if %%~xa==.scenario (
		echo: !s!: %%~nxa
		REM ~nx before the variable means name and extension. ~n means just name
		set scenarios[!s!]=%%~na
		set /A s+=1
	)
)

if !s!==0 (
	echo      _
	echo     ^| ^|   Whoops^^!
	echo     ^|_^|   No scenario files found here^^! Please choose a
	echo      _    different map folder or add at least one scenario file
	echo     ^(_^)   and try again...
	echo.
	pause
	goto select_map
) else (
	set "map=!folders[%maps_input%]!"
)

echo.
set /p scenario_input= !scenario_message!

REM check if scenario input is a valid number
set /a test_scenario_input=scenario_input
if !test_scenario_input! EQU 0 (
  if !scenario_input! EQU 0 (
    goto valid_scenario
  ) else (
    goto invalid_scenario
  )
) else (
	REM the variable s is increased one extra time after the last scenario is found
	REM so we need to check that the input is greater than or equal to 0, and less than s
	if !scenario_input! GEQ 0 (
		if !scenario_input! LSS !s! (
			goto valid_scenario
		) else (
			goto invalid_scenario
		)
	) else (
		goto valid_scenario
	)
)

:invalid_scenario
set "scenario_message=You did not enter a valid scenario number. Please try again: "
goto select_scenario

:valid_scenario
set "scenario=!scenarios[%scenario_input%]!"
REM echo.

:copy_scenario
REM get timestamp (uses javascript at bottom of this file)
for /f "tokens=* usebackq" %%a in (`start /b cscript //nologo "%~f0?.wsf"`) do (set timestamp=%%a)

REM - Copy scenario to new file, with timestamp appended.
REM - Use substring ~0,-3 to trim milliseconds, resulting in seconds.
set scenario_post=%scenario%_%timestamp:~0,-3%
REM - >nul suppresses the filename and "1 File(s) copied" lines appearing after the xcopy operation
REM   but there are JACKED UP errors related to Batch's parser? avoiding nul outputs where possible
xcopy "%tags_folder%\%maps_path%\%map%\%scenario%.scenario" "%tags_folder%\%maps_path%\%map%\%scenario%_%timestamp:~0,-3%.scenario*"

echo         __
echo        / /  Your scenario file: %tags_folder%\%maps_path%\%map%\%scenario%.scenario,
echo   __  / /   has been copied to: %tags_folder%\%maps_path%\%map%\%scenario_post%.scenario,
echo   \ \/ /
echo    \__/     which will be modified...
@TIMEOUT /t 1 /nobreak>nul

set scenario=%scenario_post%
set scenario_path="%maps_path%\%map%\%scenario%.scenario"

:choose_action
REM - Let user choose next action
echo.
echo What would you like to do?
echo.
echo  [1] Set tags folder
echo  [2] Select map
echo  [3] Select scenario
echo  [4] Inject spawn markers
echo  [5] Inject randoms geometry
echo  [6] Inject powerup waypoints
echo  [7] Exit
echo.
set /p action_input= Choose a number, then press [Enter]: 
if "%action_input%"=="1" goto set_tags_folder
if "%action_input%"=="2" goto select_map
if "%action_input%"=="3" goto select_scenario
if "%action_input%"=="4" goto inject_spawns
if "%action_input%"=="5" goto inject_randoms
if "%action_input%"=="6" goto inject_waypoints
if "%action_input%"=="7" goto goodbye



:inject_spawns
echo.
REM - Get spawn count
for /F %%C in ('invader-edit --tags %tags_folder% %scenario_path% --count player_starting_locations') do set /A spawn_count=%%C
set /A "loop_stop=(%spawn_count%-1)"

REM - Get scenery count
for /F %%S in ('invader-edit --tags %tags_folder% %scenario_path% --count scenery') do set /A scenery_count=%%S
REM echo Scenery Count %scenery_count%

REM - Get scenery palette count
for /F %%Y in ('invader-edit --tags %tags_folder% %scenario_path% --count scenery_palette') do set /A scenery_palette_count=%%Y
REM echo Scenery Palette Count %scenery_palette_count%

REM - Get object names count
for /F %%Y in ('invader-edit --tags %tags_folder% %scenario_path% --count object_names') do set /A object_names_count=%%Y
REM echo Scenery Object Names Count %object_names_count%

REM - Loop through scenery palette, find spawn_marker_nhe index in scenery palette
set /A "palette_stop=(%scenery_palette_count%-1)"
set /A spawn_marker_index = -1
for /L %%M in (0,1,%palette_stop%) do (
	for /F "tokens=*" %%N in ('invader-edit --tags %tags_folder% %scenario_path% --get scenery_palette[%%M].name') do (
		if %%N==scenery\spawn_marker_nhe\spawn_marker_nhe.scenery set /A spawn_marker_index = %%M
	)
)

REM - If spawn_marker_nhe is not found, inject it, after alerting user
if %spawn_marker_index%==-1 (

	echo      _    "spawn_marker_nhe" was NOT found in the scenery palette!
	echo     ^| ^|
	echo     ^|_^|   It will be added, but before you continue, please verify
	echo      _    the following file exists:
	echo     ^(_^)
	echo           "%tags_folder%\scenery\spawn_marker_nhe\spawn_marker_nhe.scenery"
	echo.
	
	pause
	echo.
	
	invader-edit --tags %tags_folder% %scenario_path% ^
	 --insert scenery_palette 1 end ^
	 --set scenery_palette[end].name scenery\spawn_marker_nhe\spawn_marker_nhe.scenery
	
	set /A spawn_marker_index = %scenery_palette_count%
)

REM - Loop through spawn indices
set /A inject_index = 0
for /L %%A in (0,1,%loop_stop%) do (

	set "spawn_types="
	set "do_inject="
	
	set /a end_index=!inject_index!+%scenery_count%
	set /a object_names_index=!inject_index!+%object_names_count%
	
	REM - Check type_0
	for /F %%T in ('invader-edit --tags %tags_folder% %scenario_path% --get player_starting_locations[%%A].type_0') do (
		if %%T==all_except_ctf set do_inject=true
		if %%T==slayer set do_inject=true
		if %%T==all_except_race_ctf set do_inject=true
		if %%T==all_games set do_inject=true
		set spawn_types=!spawn_types! %%T,
	)
	
	REM - Check type_1
	for /F %%T in ('invader-edit --tags %tags_folder% %scenario_path% --get player_starting_locations[%%A].type_1') do (
		if %%T==all_except_ctf set do_inject=true
		if %%T==slayer set do_inject=true
		if %%T==all_except_race_ctf set do_inject=true
		if %%T==all_games set do_inject=true
		set spawn_types=!spawn_types! %%T,
	)
	
	REM - Check type_2
	for /F %%T in ('invader-edit --tags %tags_folder% %scenario_path% --get player_starting_locations[%%A].type_2') do (
		if %%T==all_except_ctf set do_inject=true
		if %%T==slayer set do_inject=true
		if %%T==all_except_race_ctf set do_inject=true
		if %%T==all_games set do_inject=true
		set spawn_types=!spawn_types! %%T,
	)
	
	REM - Check type_3
	for /F %%T in ('invader-edit --tags %tags_folder% %scenario_path% --get player_starting_locations[%%A].type_3') do (
		if %%T==all_except_ctf set do_inject=true
		if %%T==slayer set do_inject=true
		if %%T==all_except_race_ctf set do_inject=true
		if %%T==all_games set do_inject=true
		set spawn_types=!spawn_types! %%T,
	)
	
	if defined do_inject (
	
		for /F "tokens=*" %%P in ('invader-edit --tags %tags_folder% %scenario_path% --get player_starting_locations[%%A].position') do (
			
			REM - Add object name so the spawn point can be named
			invader-edit --tags %tags_folder% %scenario_path% --no-safeguards ^
			 --insert object_names 1 end ^
			 --set object_names[end].name "spawn_marker_nhe_%%A"
			
			invader-edit --tags %tags_folder% %scenario_path% ^
			 --insert scenery 1 end ^
			 --set scenery[end].position "%%P" ^
			 --set scenery[end].type %spawn_marker_index% ^
			 --set scenery[end].name !object_names_index!
			
		)
	
		for /F "tokens=*" %%F in ('invader-edit --tags %tags_folder% %scenario_path% --get player_starting_locations[%%A].facing') do (
			invader-edit --tags %tags_folder% %scenario_path% --set scenery[end].rotation "%%F 0 0"
		)
		
		REM - :~0,-1 is substring logic. start at 0, remove 1 char from end. this removes
		REM   the extra comma produced in the type loops above that concatenate spawn types
		echo Spawn %%A: spawn_marker_nhe_%%A injected [!spawn_types:~0,-1! ]
	
		set /A inject_index=inject_index+1
		
	) else (
		echo Spawn %%A: ignored                     [!spawn_types:~0,-1! ]
	)
)

echo         __
echo        / /  
echo   __  / /   Done^^!
echo   \ \/ /    Spawn markers injected: !inject_index!
echo    \__/     
@TIMEOUT /t 1 /nobreak>nul
goto choose_action

set use_one_anyway=false
:inject_randoms
echo.
echo Searching scenery palette...
echo.

REM - Loop through scenery palette, find index of scenery containing "random"
for /F %%Y in ('invader-edit --tags %tags_folder% %scenario_path% --count scenery_palette') do set /A scenery_palette_count=%%Y
set /A "palette_stop=(%scenery_palette_count%-1)"
set /A randoms_index=-1
set /A r=0
set "randoms_scenery_guess="
for /L %%M in (0,1,%palette_stop%) do (
	for /F "tokens=*" %%N in ('invader-edit --tags %tags_folder% %scenario_path% --get scenery_palette[%%M].name') do (
		set "scenery_path=%%N"
		set scenery_paths[!r!]=%%N
		set scenery_names[!r!]=%%~nN
		REM - This magically searches a string for another string
		If /I Not "!scenery_path!"=="!scenery_path:random=!" (
			set /A randoms_index = %%M
			set randoms_scenery_guess=%%~nN
			echo  [%%M] %%~nN - maybe randoms
		) else (
			echo  [%%M] %%~nN
		)
		set /A r+=1
	)
)

if defined randoms_scenery_guess (
	echo.
	echo "%randoms_scenery_guess%" was found in your scenery palette.
	set /p randoms_input= Press [Enter] to use it, or type a different number: 
	
	if !randoms_input!=="" (
		set randoms_input=!randoms_index!
	)
	
	:test_randoms_selection
	REM check if randoms_input is a valid number
	set /a test_randoms_input=randoms_input
	if !test_randoms_input! EQU 0 (
	  if !randoms_input! EQU 0 (
		goto valid_randoms
	  ) else (
		goto invalid_randoms
	  )
	) else (
		REM the variable r is increased one extra time after the last scenario is found
		REM so we need to check that the input is greater than or equal to 0, and less than r
		if !randoms_input! GEQ 0 (
			if !randoms_input! LSS !r! (
				goto valid_randoms
			) else (
				goto invalid_randoms
			)
		) else (
			goto valid_randoms
		)
	)
	
) else (
	
	echo.
	echo Could not confidently guess the randoms scenery. You have 3 options:
	echo.
	echo  - Manually update your scenery palette in guerilla, THEN press [R][Enter] to Reselect your scenario.
	echo  - Press [F][Enter] to Find all .scenery files containing "random" in "%tags_folder%" subfolders.
	echo  - Enter a number from the list above to use an existing scenery item in the palette.
	echo.
	set /p options_input= Enter [R], [F], or a valid number: 
	
	if !options_input!==r (
		goto select_scenario
	) else if !options_input!==R (
		goto select_scenario
	) else if !options_input!==f (
		goto search_tags_for_randoms
	) else if !options_input!==F (
		goto search_tags_for_randoms
	) else (
		REM set use_one_anyway=true
		set randoms_input=!options_input!
		set /a selected_anyway=!options_input!
		goto test_randoms_selection
	)
	pause
)
echo.

:invalid_randoms
echo.
echo  There was an error...
goto inject_randoms

:valid_randoms
REM echo.
REM echo !scenery_paths[%randoms_input%]! !scenery_names[%randoms_input%]!

REM - Set randoms scenery offset
set randoms_path=!scenery_paths[%randoms_input%]!
:valid_randoms_shortcut
for /F "tokens=*" %%P in ('invader-edit --tags %tags_folder% !randoms_path! --get origin_offset') do set randoms_origin_offset=%%P
REM echo.
set /A w=0
for %%y in (%randoms_origin_offset%) do (

	REM - Batch can't do float math, but we can add or remove negative sign by checking string length.
    REM   Negative position values in halo tags are always 9 characters, positives are 8.
    REM   So we act accordingly:
	
	set value=%%y
	
	REM - Get character length of this position value
	for /L %%n in (1 1 500) do if "!value:~%%n,1!" neq "" set /a "poslen=%%n+1"
	if !value! == 0.000000 (
		REM - No need to invert 0
	) else if !value! == -0.000000 (
		REM - "Negative Zero" is better expressed as just Zero
		set value=0.000000
	) else (
		if !poslen! == 9 (
			REM - 9 characters, must be negative. Use substring to remove the leading hyphen.
			set value=!value:~1!
		) else (
			REM - Not 9 characters, must be positive. Add a negative sign.
			set value=-!value!
		)
	)
	set randoms_offset_xyz[!w!]=!value!
	REM echo !w! %%y is now !value!
	set /A w+=1
)

REM - Get scenery count
for /F %%Y in ('invader-edit --tags %tags_folder% %scenario_path% --count scenery') do set /A scenery_count=%%Y

REM - Get object names count
for /F %%O in ('invader-edit --tags %tags_folder% %scenario_path% --count object_names') do set /A object_names_count=%%O

REM - Add object name so the randoms scenery can be named
invader-edit --tags %tags_folder% %scenario_path% --no-safeguards ^
 --insert object_names 1 end ^
 --set object_names[end].name "!scenery_names[%randoms_input%]!"
	 
invader-edit --tags %tags_folder% %scenario_path% ^
 --insert scenery 1 end ^
 --set scenery[end].position "!randoms_offset_xyz[0]! !randoms_offset_xyz[1]! !randoms_offset_xyz[2]!" ^
 --set scenery[end].type %randoms_input% ^
 --set scenery[end].name %object_names_count%

echo         __
echo        / /
echo   __  / /   !scenery_names[%randoms_input%]! added to scenery.
echo   \ \/ /    position inverted to [!randoms_offset_xyz[0]!, !randoms_offset_xyz[1]!, !randoms_offset_xyz[2]!]
echo    \__/  
@TIMEOUT /t 1 /nobreak>nul
 
goto choose_action


:search_tags_for_randoms
REM - Get current directory character length, plus tags_folder, plus a backslash
REM   so we can remove that many characters from the scenery files discovered
for /L %%n in (1 1 500) do if "!__cd__:~%%n,1!" neq "" set /a "len=%%n+1"
for /L %%n in (1 1 50) do if "!tags_folder:~%%n,1!" NEQ "" set /a "andlen=%%n+1"
set /a "fullen=%len%+%andlen%+1"
set /a scenery_count=0
echo.
for /r . %%g in (*random*.scenery) do (
	set "absPath=%%g"
	set "relPath=!absPath:~%fullen%!"
	set "found_scens[!scenery_count!]=!absPath:~%fullen%!"
	echo( [!scenery_count!] !relPath!
	set /a scenery_count+=1
)

echo.
set /p randoms_input= Choose a scenery item by number and press [Enter]: 

REM check if randoms_input is a valid number
set /a test_randoms_input=randoms_input

if !randoms_input!=="" goto invalid_randoms
if !randoms_input! LSS 0 goto invalid_randoms

if !test_randoms_input! EQU 0 (
  if !randoms_input! EQU 0 (
	goto add_randoms_to_palette
  ) else (
	goto invalid_randoms
  )
) else (
	REM the variable scenery_count is increased one extra time after the last scenario is found
	REM so we need to check that the input is greater than or equal to 0, and less than scenery_count
	if !randoms_input! GEQ 0 (
		if !randoms_input! LSS !scenery_count! (
			goto add_randoms_to_palette
		) else (
			goto invalid_randoms
		)
	) else (
		goto add_randoms_to_palette
	)
)

:add_randoms_to_palette

invader-edit --tags %tags_folder% %scenario_path% ^
 --insert scenery_palette 1 end ^
 --set scenery_palette[end].name "!found_scens[%randoms_input%]!"

echo         __
echo        / /
echo   __  / /   !found_scens[%randoms_input%]!
echo   \ \/ /    was added to the palette. 
echo    \__/     
@TIMEOUT /t 1 /nobreak>nul

for /F %%Y in ('invader-edit --tags %tags_folder% %scenario_path% --count scenery_palette') do set /A scenery_palette_count=%%Y

set "randoms_path=!found_scens[%randoms_input%]!"
set /a "randoms_input=!scenery_palette_count!-1"
for /F "tokens=*" %%N in ('invader-edit --tags %tags_folder% %scenario_path% --get scenery_palette[end].name') do (
	set scenery_names[%randoms_input%]=%%~nN
)

goto valid_randoms_shortcut


:inject_waypoints
REM - Get netgame equipment count
for /F %%Y in ('invader-edit --tags %tags_folder% %scenario_path% --count netgame_equipment') do set /A netgame_equipment_count=%%Y
echo.
echo Looking for relevant powerups in netgame equipment...
echo.
REM - Loop through netgame equipment, find powerups
set /A "equipment_stop=(%netgame_equipment_count%-1)"
REM - Set /A spawn_marker_index = -1
set "rocket=item collections\single weapons\rocket launcher.item_collection"
set "camo=item collections\powerups\powerup invisibility.item_collection"
set "overshield=item collections\powerups\powerup super shield.item_collection"
set "sniper=item collections\single weapons\sniper rifle.item_collection"
set "oscamo=item collections\powerups\shield-invisibility.item_collection"

set /A waypoints_injected = 0
for /L %%N in (0,1,%equipment_stop%) do (

	set "equipment_types="
	set "equipment_name="
	set "waypoint_name="
	set "do_inject="
	
	for /F "tokens=*" %%E in ('invader-edit --tags %tags_folder% %scenario_path% --get netgame_equipment[%%N].item_collection') do (
		
		set "check_type="
		
		if %%E==!rocket! (
			set check_type=true
			set waypoint_name=rocket_flag
			set equipment_name="rocket launcher"     
		)
		if %%E==!camo! (
			set check_type=true
			set waypoint_name=camo_flag
			set equipment_name="powerup invisibility"
		)
		if %%E==!overshield! (
			set check_type=true
			set waypoint_name=overshield_flag
			set equipment_name="powerup super shield"
		)
		if %%E==!sniper! (
			set check_type=true
			set waypoint_name=sniper_flag
			set equipment_name="sniper rifle"        
		)
		if %%E==!oscamo! (
			set check_type=true
			set waypoint_name=oscamo_flag
			set equipment_name="shield-invisibility" 
		)
		
		if defined check_type (
			REM check type_0
			for /F %%T in ('invader-edit --tags %tags_folder% %scenario_path% --get netgame_equipment[%%N].type_0') do (
				if %%T==all_except_ctf set do_inject=true
				if %%T==slayer set do_inject=true
				if %%T==all_except_race_ctf set do_inject=true
				if %%T==all_games set do_inject=true
				set equipment_types=!equipment_types! %%T,
			)
			
			REM check type_1
			for /F %%T in ('invader-edit --tags %tags_folder% %scenario_path% --get netgame_equipment[%%N].type_1') do (
				if %%T==all_except_ctf set do_inject=true
				if %%T==slayer set do_inject=true
				if %%T==all_except_race_ctf set do_inject=true
				if %%T==all_games set do_inject=true
				set equipment_types=!equipment_types! %%T,
			)
			
			REM check type_2
			for /F %%T in ('invader-edit --tags %tags_folder% %scenario_path% --get netgame_equipment[%%N].type_2') do (
				if %%T==all_except_ctf set do_inject=true
				if %%T==slayer set do_inject=true
				if %%T==all_except_race_ctf set do_inject=true
				if %%T==all_games set do_inject=true
				set equipment_types=!equipment_types! %%T,
			)
			
			REM check type_3
			for /F %%T in ('invader-edit --tags %tags_folder% %scenario_path% --get netgame_equipment[%%N].type_3') do (
				if %%T==all_except_ctf set do_inject=true
				if %%T==slayer set do_inject=true
				if %%T==all_except_race_ctf set do_inject=true
				if %%T==all_games set do_inject=true
				set equipment_types=!equipment_types! %%T,
			)
		)
	)
	
	if defined do_inject (
	
		for /F "tokens=*" %%P in ('invader-edit --tags %tags_folder% %scenario_path% --get netgame_equipment[%%N].position') do (
			
			invader-edit --tags %tags_folder% %scenario_path% ^
			 --insert cutscene_flags 1 end ^
			 --set cutscene_flags[end].position "%%P" ^
			 --set cutscene_flags[end].name !waypoint_name!
		)
	
		set /A waypoints_injected=waypoints_injected+1
		
		REM - :~0,-1 is substring logic. start at 0, remove 1 char from end. this removes
		REM   the extra comma produced in the type loops above that concatenate spawn types
		echo   !waypoints_injected!: !equipment_name! [!equipment_types:~0,-1! ]  "!waypoint_name!" injected.
		
	) else (
		REM echo Equipment %%E: ignored                   [!equipment_types:~0,-1! ]
	)
)


set "ess=s were"
if !waypoints_injected!==0 (
	echo      _
	echo     ^| ^|
	echo     ^|_^|   !waypoints_injected! cutscene flag%ess% injected.
	echo      _    Not sure what happened there.
	echo     ^(_^)
) else if !waypoints_injected!==1 (
	set "ess= was"
)

echo         __
echo        / /
echo   __  / /   !waypoints_injected! cutscene flag%ess% were injected.
echo   \ \/ /    That was fun.
echo    \__/  
@TIMEOUT /t 1 /nobreak>nul
goto choose_action


endlocal


:goodbye
echo.
echo      Goodbye!
echo.
sleep 2
exit

 
REM - Get unix time using javascript for copying and appending to scenario file
<job><script language="JavaScript">
  WScript.Echo(new Date().getTime());
</script></job>