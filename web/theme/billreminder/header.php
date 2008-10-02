<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" <?php language_attributes(); ?>>

<head profile="http://gmpg.org/xfn/11">
<meta http-equiv="Content-Type" content="<?php bloginfo('html_type'); ?>; charset=<?php bloginfo('charset'); ?>" />

<title><?php bloginfo('name'); ?> <?php if ( is_single() ) { ?> &raquo; Blog Archive <?php } ?> <?php wp_title(); ?></title>

<link rel="stylesheet" href="<?php bloginfo('stylesheet_url'); ?>" type="text/css" media="screen" />
<link rel="alternate" type="application/rss+xml" title="<?php bloginfo('name'); ?> RSS Feed" href="<?php bloginfo('rss2_url'); ?>" />
<link rel="pingback" href="<?php bloginfo('pingback_url'); ?>" />
<link rel="shortcut icon" href="<?php bloginfo('template_directory'); ?>/images/icon.gif" />

<script type="text/javascript" src="<?php bloginfo('template_directory'); ?>/js/jquery.min.js"></script>
<script type="text/javascript" src="<?php bloginfo('template_directory'); ?>/js/billreminder.js"></script>

<?php wp_head(); ?>
</head>
<body>
<div id="page">


<div id="header">
	<div id="logo">
	</div>

	<div id="titulo">
		<h1><a href="<?php echo get_option('home'); ?>/" title="<?php bloginfo('name'); ?>"><span><?php bloginfo('name'); ?></span></a></h1>
	</div>

	<div id="menu">
		<ul>
			<li>
				<a href="#" id="about" title="About">About</a>
			</li>
			<li>
				<a href="<?php echo get_option('home'); ?>/" id="home" title="<?php bloginfo('name'); ?>">Home</a>
			</li>
			<li>
				<a href="#" id="download" title="Get BillReminder">Download</a>
			</li>
			<li>
				<a href="<?php echo get_option('home'); ?>/#content" id="news" title="Lastest News about BillReminder">News</a>
			</li>
			<li>
				<a href="#" id="development" title="Do you want contribute?">Development</a>
			</li>
			<li>
				<a href="#" id="translate" title="BillReminder in your language">Translate</a>
			</li>
		</ul>
	</div>

<div id="destaque">
            <div id="crop">
                <div class="widearea">
                		<div class="featured-item">
                        <h3>About</h3>
                        <?php
                        	$about = & get_post($page=2);
                        	print $about->post_content;
                        ?>
                    </div>
                    <div class="featured-item">
                        <h3>Download</h3>
                        <?php
                        	$download = & get_post($page=26);
                        	print $download->post_content;
                        ?>
                    </div>
                    <div class="featured-item">
                        <h3>Development</h3>
                        <?php
                        	$development = & get_post($page=28);
                        	print $development->post_content;
                        ?>
                    </div>
                    <div class="featured-item">
                        <h3>Translate</h3>
                        <?php
                        	$translate = & get_post($page=30);
                        	print $translate->post_content;
                        ?>
                    </div>
                </div>
            </div>
        </div>
</div>
