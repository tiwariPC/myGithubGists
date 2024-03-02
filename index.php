<style>
.heading-line {
  margin-left: 0;
}
</style>
<?php
$pwd = preg_replace("|^\/((\w)\w+)\/|","/eos/user/$2/$1/www/",$_SERVER["REQUEST_URI"]);
$pwd = preg_replace("(\?.*)","",$pwd);
preg_match("|^\/(\w+)\/|",$_SERVER["REQUEST_URI"],$usr);
$pwdshort = preg_replace("(.*www/)","$usr[1]/",$pwd);
chdir($pwd);
?>
<html>
<head>
<title><?php echo $pwdshort; ?></title>
<link rel="SHORTCUT ICON" type="image/x-icon" href="https://ineuteli.web.cern.ch/ineuteli/favicon.ico"/>
<style type='text/css'>
  body {
    font-family: "Candara", sans-serif;
    font-size: 9pt;
    line-height: 10.5pt;
  }
  div.pic {
    display: block;
    float: left;
    background-color: white;
    border: 1px solid #ccc;
    padding: 2px;
    text-align: left;
    margin: 2px 12px 12px 2px;
    -moz-box-shadow: 6px 4px 4px rgb(80,80,90);    /* Firefox 3.5 */
    -webkit-box-shadow: 6px 4px 4px rgb(80,80,90); /* Chrome, Safari */
    box-shadow: 2px 6px 2px rgb(80,80,90);         /* New browsers */
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  div.pic h3 {
    font-size: 9pt;
    margin: 0.5em 1em 0.2em 1em;
  }
  div.pic p {
    font-size: 11pt;
    margin: 0.2em 1em 0.1em 1em;
  }
  div.pic .pics{
    display: block;
    float: left;
    background-color: white;
    border: 1px solid #ccc;
    padding: 2px;
    text-align: center;
    margin: 4px 4px 4px 4px;
    -moz-box-shadow: 6px 4px 4px rgb(80,80,90);    /* Firefox 3.5 */
    -webkit-box-shadow: 6px 4px 4px rgb(80,80,90); /* Chrome, Safari */
    box-shadow: 1px 1px 1px rgb(80,80,90);         /* New browsers */
    width: 320px;
    min-height: 330px;
    max-height: 380px;
  }

  div.pic .pics .img-wrapper {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 10px;
  }

  h1 { color: rgb(40,40,80); }
  h2 { padding-top: 5pt; }
  h2 a { color: rgb(20,20,100); }
  h3 a { color: rgb(40,40,120); }
  a { text-decoration: none; color: rgb(50,50,150); }
  a:hover { text-decoration: underline; color: rgb(80,80,250); }
  div.dirlinks h2 { padding-top: 0pt; margin-bottom: 4pt; margin-left: -15pt; color: rgb(20,20,80); }
  div.dirlinks { margin: 0 15pt; }
  div.dirlinks a {
    font-size: 11pt; font-weight: bold;
    padding: 0 0.5em;
  }
  pre {
    font-family: monospace;
    max-width:1000px;
    white-space: pre-wrap;     /* css-3 */
    white-space: -moz-pre-wrap !important; /* Mozilla */
    white-space: -pre-wrap;    /* Opera 4-6 */
    white-space: -o-pre-wrap;  /* Opera 7 */
    word-wrap:   break-word;   /* Internet Explorer 5.5+ */
  }
</style>
</head>
<body>
<h1><?php echo $pwd;?></h1>
<!-- <h1><?php echo getcwd();?></h1> -->
<?php
$has_subs = false;
foreach(glob("*") as $filename){
    if(is_dir($filename) && !preg_match("/^\..*|.*private.*/", $filename)){
      $has_subs = true;
      break;
    }
}
if($has_subs){
    print "<div class=\"dirlinks\">\n";
    print "<h2>Directories</h2>\n";
    print "<a href=\"../\">[parent]</a> ";
    print "</div>";
}else{
    print "<div class=\"dirlinks\">\n";
    print "<h2><a href=\"../\">[parent]</a></h2>";
    print "</div>";
}
?>
<h2><a name="plots">Plots</a></h2>
<p><form>Filter: <input type="text" name="match" size="30" value="<?php if(isset($_GET['match'])) print htmlspecialchars($_GET['match']); ?>" /><input type="Submit" value="Go" /><input type="checkbox"  name="regexp" <?php if($_GET['regexp']) print "checked=\"checked\""?> >RegExp</input></form></p>
<div>
<?php
$dir = ".";
$allowed_extensions = array("png");
$other_exts = array('.pdf','.jpg','.jpeg','.jpg','.cxx','.eps','.root','.txt','.tex','.log','.dir','.info','.psd');
$subdirs = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir), RecursiveIteratorIterator::SELF_FIRST);
$has_matching_image_files = false;

foreach ($subdirs as $subdir) {
  if ($subdir->isDir() && !in_array($subdir->getBasename(), array('.', '..'))) {
    $subdir_name = $subdir->getBasename();
    $displayed = array(); // Initialize the $displayed array
    $files = new DirectoryIterator($subdir->getPathname());
    foreach ($files as $file) {
      if ($file->isFile()) {
        $full_path = $file->getPathname();
        $file_extension = strtolower($file->getExtension());
        if (in_array($file_extension, $allowed_extensions)) {
          if (isset($_GET['match'])) {
            $keywords = explode("+", $_GET['match']);
            foreach ($keywords as $keyword) {
              if (isset($_GET['regexp']) && $_GET['regexp']) {
                if (!preg_match('/.*' . $keyword . '.*/', $full_path)) {
                  continue 2; // Skip to the next iteration of the outer loop
                }
              } else {
                if (!fnmatch('*' . $keyword . '*', $full_path)) {
                  continue 2; // Skip to the next iteration of the outer loop
                }
              }
            }
          }
          $has_matching_image_files = true;
          break;
        }
      }
    }

    if ($has_matching_image_files) {
      // Print the directory and its matching image files
      print "<div class='pic'>\n";
      echo '<hr><hr>';
      echo '<span class="heading-line"><p style="text-align: left;"><h2>' . $subdir->getPathname() . '</h2></p></span>';
      echo '<hr>';
      foreach ($files as $file) {
        if ($file->isFile()) {
          $full_path = $file->getPathname();
          $file_extension = strtolower($file->getExtension());
          $filename = $file->getFilename();
          if (in_array($file_extension, $allowed_extensions)) {
            if(isset($_GET['match'])){
              $keywords = split("+",$_GET['match']);
              //foreach($keywords as $keyword){
                if(isset($_GET['regexp']) && $_GET['regexp']){
                  if(!preg_match('/.*'.$_GET['match'].'.*/', $full_path)) continue;
                }else{
                  if(!fnmatch('*'.$_GET['match'].'*', $full_path)) continue;
                }
              //}
            }
            array_push($displayed, $full_path);
            $brfname = str_replace("_","_<wbr>",$filename); //&shy;
            print "<div class='pics'>\n";
            print "<div class='img-wrapper'>\n";
            print "<h3><a href=\"$full_path\">$brfname</a></h3>";
            print "<a href=\"$full_path\"><img src=\"$full_path\" style=\"border: none; max-width: 300px; max-height: 360px; \"></a>";
            $others = array();
            foreach($other_exts as $ex){
                $other_filename = str_replace('.png', $ex, $full_path);
                if(file_exists($other_filename)){
                  array_push($others, "<a class=\"file\" href=\"$other_filename\">[" . $ex . "]</a>");
                  if($ex != '.txt') array_push($displayed, $other_filename);
                }
            }
            // print "<br>";
            if($others) print "<p>Also as ".implode(', ',$others)."</p>";
            print "</div>";
            print "</div>";
          }
        }
      }
      print "</div>";
    }

    // Reset the flag for the next iteration
    $has_matching_image_files = false;
    unset($files);
  }
}
?>

<br>
</body>
</html>