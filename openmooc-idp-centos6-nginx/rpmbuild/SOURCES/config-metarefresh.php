<?php

include_once('/etc/simplesamlphp/config/openmooc_components.php');

$config['sets'] = array();

foreach ($components as $key => $url) {

    $config['sets'][$key] = array (
                                    'cron'		=> array('metarefresh'),
                                    'sources'	=> array(
                                        array(
                                            'src' => $url,
                                            #'validateFingerprint' => '',
                                        ),
                                    ),
                                    'expireAfter' 		=> 60*60*24*1, // Maximum 1 days cache time.
                                    'outputDir' 	=> "metadata/$key/",
                                    'outputFormat' => 'flatfile',
		                    );
}
