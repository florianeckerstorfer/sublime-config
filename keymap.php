<?php

require_once 'JSON.php';

$dir = new RecursiveDirectoryIterator(__DIR__);

// Filter "*.sublime-keymap" files
$files = new RecursiveCallbackFilterIterator($dir, function (SplFileInfo $current, $key, $iterator) {
    // Allow recursion
    if ($iterator->hasChildren()) {
        return TRUE;
    }
    // Check for keymap files
    if ($current->isFile() && preg_match('/\.sublime-keymap$/', $current->getFilename())) {
        return TRUE;
    }
    return FALSE;
});

$windows    = [];
$osx        = [];
$linux      = [];

foreach (new RecursiveIteratorIterator($files) as $file) {
    if (preg_match('/\(Linux\)/', $file->getPathname())) {
        $linux[] = $file;
    } elseif (preg_match('/\(OSX\)/', $file->getPathname())) {
        $osx[] = $file;
    } elseif (preg_match('/\(Windows\)/', $file->getPathname())) {
        $windows[] = $file;
    } else {
        $linux[] = $file;
        $osx[] = $file;
        $windows[] = $file;
    }
}

if ('Darwin' === PHP_OS) {
    $files = $osx;
} elseif (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
    $files = $windows;
} else {
    $files = $linux;
}

function json_last_error_message() {
    switch (json_last_error()) {
        case JSON_ERROR_NONE:
            return 'No errors';
        break;
        case JSON_ERROR_DEPTH:
            return 'Maximum stack depth exceeded';
        break;
        case JSON_ERROR_STATE_MISMATCH:
            return 'Underflow or the modes mismatch';
        break;
        case JSON_ERROR_CTRL_CHAR:
            return 'Unexpected control character found';
        break;
        case JSON_ERROR_SYNTAX:
            return 'Syntax error, malformed JSON';
        break;
        case JSON_ERROR_UTF8:
            return 'Malformed UTF-8 characters, possibly incorrectly encoded';
        break;
        default:
            return 'Unknown error';
        break;
    }
}

$keymap = [];

foreach ($files as $file) {
    $package = basename($file->getPath());
    $content = file_get_contents($file->getPathname());
    $json = new Services_JSON(SERVICES_JSON_LOOSE_TYPE);
    $mappings = $json->decode($content);
    if (!is_array($mappings)) {
        printf("Could not find keymap for package '%s'.\n", $package);
        continue;
    }
    foreach ($mappings as $mapping) {
        $key = implode(',', $mapping['keys']);

        $command = $mapping['command'];
        if (!isset($keymap[$key])) {
            $keymap[$key] = [];
        }
        $keymap[$key][] = [
            'command'       => $command,
            'package'       => $package,
            'args'          => $mapping['args'],
            'context'       => $mapping['context']
        ];
    }
}

foreach ($keymap as $key => $mappings) {
    printf("%s\n", $key);
    foreach ($mappings as $mapping) {
        printf("  - %s: %s\n", $mapping['package'], $mapping['command']);
    }
}
