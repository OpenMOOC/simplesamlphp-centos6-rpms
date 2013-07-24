<?php

include_once('/etc/simplesamlphp/config/openmooc_components.php');

$config['enable.saml20-idp'] = true;
$config['theme.use'] = 'sspopenmooc:openmooc';

foreach ($components as $key => $url) {
    $config['metadata.sources'][] = array('type' => 'flatfile', 'directory' => "metadata/$key");
}


