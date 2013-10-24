<?php

include_once('/etc/simplesamlphp/config/openmooc_components.php');

$config['enable.saml20-idp'] = true;
$config['theme.use'] = 'sspopenmooc:openmooc';

foreach ($components as $component) {
	foreach ($component as $key => $url) {
	    $config['metadata.sources'][] = array('type' => 'flatfile', 'directory' => "/var/lib/simplesamlphp/metadata/$key");
	}
}


