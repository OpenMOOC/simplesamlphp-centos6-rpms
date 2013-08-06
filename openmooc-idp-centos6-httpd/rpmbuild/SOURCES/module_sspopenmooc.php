<?php

	// Domain of our MoocNG component
	$mooc_domain = 'mooc.example.com';

	// Domain of the IdP
	$idp_domain = 'idp.example.com';

	$config = array(

		  'urls' => array (
		          'site' => 'https://'.$mooc_domain,
		          'login' => "https://$mooc_domain/saml2/login/",
		          'logout' => "https://$mooc_domain/saml2/logout/",
		          'register' => "https://$idp_domain/simplesaml/module.php/userregistration/newUser.php",
		          'forgotpassword' => "https://$idp_domain/simplesaml/module.php/userregistration/lostPassword.php",
		          'changepassword' => "https://$idp_domain/simplesaml/module.php/userregistration/changePassword.php",
		          'profile' => "https://$idp_domain/simplesaml/module.php/userregistration/reviewUser.php",
		          'legal' => "https://$mooc_domain/legal",
		          'tos' => "https://$mooc_domain/legal/#tos",
		          'copyright' => "#",
		  ),

		  // Internal file (Ex.  default.css)  or external (Ex. //example.com/css/default.css)
		  // (Notice that // will respect the http/https protocol,
		  //  load elements with different protocol than main page produce warnings on some browser)
		  'cssfile' => 'default.css',
		  'bootstrapfile' => 'bootstrap.css',
		  'imgfile' => 'logo.png',
		  'title' => 'OpenMOOC',
		  'slogan' => 'Knowledge for the masses',
	);
?>

