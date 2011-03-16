#!/usr/bin/perl
$|=1;
use Image::Magick;

$mediumwidth=450;
$thumbnailwidth=200;
$sqthumbnailwidth=100;

$dir = "/var/www/growse.com/ocukimages";

opendir(my $dh,$dir) || die "Can't open $dir";
@fullimages = grep {/FULL\.jpg/ && -f "$dir/$_"} readdir($dh);
closedir($dh);

foreach (@fullimages) {
	my $m = $_;
	my $t = $_;
	my $sq = $_;
	my $mpresent=0;
	my $tpresent=0;
	my $sqpresent=0;
	$m=~s/_FULL\.jpg/_MEDIUM\.jpg/gi;
	$t=~s/_FULL\.jpg/_THUMBNAIL\.jpg/gi;
	$sq=~s/_FULL\.jpg/_SQTHUMBNAIL\.jpg/gi;
	my $image=undef;
	if ( -f "$dir/$m") {
		$mpresent=1;
	}

	if ( -f "$dir/$t") {
		$tpresent=1;
	}

	if ( -f "$dir/$sq") {
		$sqpresent=1;
	}

	if ($mpresent+$tpresent+$sqpresent lt 3) {
		$image = Image::Magick->new;
		$error = $image->Read("$dir/$_");
		if ($error eq undef) {
			if ($mpresent eq 0) {
				my $mediumimage=$image->Clone();
				&resizeImage($mediumimage,$mediumwidth);
				$mediumimage->Strip();
				print "Writing $dir/$m\n";
				open(FILE,">$dir/$m")  || warn "Can't open $m for writing";
				binmode FILE;
				$mediumimage->Write(file=>\*FILE,filename=>$dir/$m);
				close FILE;
			}
			if ($tpresent eq 0) {
				my $thumbnailimage=$image->Clone();
				&resizeImage($thumbnailimage,$thumbnailwidth);
				$thumbnailimage->Strip();
				print "Writing $dir/$t\n";
				open(FILE,">$dir/$t")  || warn "Can't open $t for writing";
				binmode FILE;
				$thumbnailimage->Write(file=>\*FILE,filename=>$dir/$t);
				close FILE;
			}
			if ($sqpresent eq 0) {
				my $sqthumbnailimage = $image->Clone();
				&resizeImageWithCrop($sqthumbnailimage,$sqthumbnailwidth);
				$sqthumbnailimage->Strip();
				print "Writing $dir/$sq\n";
				open(FILE,">$dir/$sq") || warn "Can't open $sq for writing";
				binmode FILE;
				$sqthumbnailimage->Write(file=>\*FILE,filename=>$dir/$sq);
				close FILE;
			}
		}
	}
}
exit();
print "Starting loop\n";
while (($id,$type,$entry)= $sth->fetchrow_array) {
	print "$id $type $entry\n";


	#Fetch the image from the database
	$sth2->bind_param(1,$id);
	$sth2->execute();
	my @imageblob = $sth2->fetchrow_array();
	my $image = Image::Magick->new(magick=>'jpg');
	$error = $image->BlobToImage(@imageblob);
	if (!$error) {

		#First see what thumbnails exist and what needs to be generated
		$sth3->bind_param(1,$entry);
		$sth3->execute();
		#Generate medium thumbnail if it's not present
		my $mpresent = 0;
		my $spresent = 0;
		my $ssqpresent = 0;
		my $types = $sth3->fetchall_arrayref([0]);
		foreach (@{$types}) {
			print "FOUND: $$_[0]\n";
			if ($$_[0] eq 'MEDIUM') {
				$mpresent=1;
			}
			if ($$_[0] eq 'THUMBNAIL') {
				$spresent=1;
			}
			if($$_[0] eq 'SQTHUMBNAIL') {
				$ssqpresent=1;
			}
		}
	
		if ($mpresent eq 0) {
			print "\tMedium image not found. Generating\n";
			my $mediumimage = $image->Clone();
			&resizeImage($mediumimage,$mediumwidth);
			$insertsth->bind_param(1,'MEDIUM');
			$insertsth->bind_param(2,$entry);
			$insertsth->bind_param(3,$mediumimage->ImageToBlob(), { pg_type => DBD::Pg::PG_BYTEA });
			$insertsth->execute();
			print "\tMedium image generated and inserted\n";
		}

		if ($spresent eq 0) {
			print "\tThumbnail image not found. Generating\n";
			my $thumbnailimage = $image->Clone();
			&resizeImage($thumbnailimage,$thumbnailwidth);
			$insertsth->bind_param(1,'THUMBNAIL');
			$insertsth->bind_param(2,$entry);
			$insertsth->bind_param(3,$thumbnailimage->ImageToBlob(), { pg_type => DBD::Pg::PG_BYTEA });
			$insertsth->execute();
			print "\tThumbnail image generated and inserted\n";
		}

		if ($spresent eq 0) {
			print "\tSquare Thumbnail image not found. Generating\n";
			my $sqthumbnailimage = $image->Clone();
			&resizeImageWithCrop($sqthumbnailimage,$sqthumbnailwidth);
			$insertsth->bind_param(1,'SQTHUMBNAIL');
			$insertsth->bind_param(2,$entry);
			$insertsth->bind_param(3,$sqthumbnailimage->ImageToBlob(), { pg_type => DBD::Pg::PG_BYTEA });
			$insertsth->execute();
			print "\tSquare Thumbnail image generated and inserted\n";
		}
	} else {
		print STDERR "Error generated reading image: $error";
	}
	print "\n";
}

#$dbh->rollback();
$dbh->commit();

sub resizeImage {
	my$image=shift;
	my$maxwidth=shift;
	my $width = $image->Get('width');
	my $height = $image->Get('height');
	if ($width>maxwidth) {
		my $scalepercent = $maxwidth / $width;
		my $newwidth=$maxwidth;
		my $newheight = $height*$scalepercent;
		$image->Resize(width=>$newwidth,height=>$newheight,filter=>'Lanczos');
		$image->Set(quality=>75);
	}
	return $image;
}

sub resizeImageWithCrop {
	my $image=shift;
	my $cropsize=shift;
	my $width=$image->Get('width');
	my $height=$image->Get('height');
	my $scale;
	my $newwidth;
	my $newheight;
	if ($width>$height) {
		$scale = $cropsize/$height;
		$newwidth = $scale*$width;
		$newheight=$cropsize;
	} else {
		$scale = $cropsize/$width;
		$newheight = $scale*$height;
		$newwidth=$cropsize;
	}
	$image->Resize(width=>$newwidth,height=>$newheight,filter=>'Lanczos');
	$image->Set(Gravity=>'Center');
	$image->Crop(geometry=>$cropsize.'x'.$cropsize);
	$image->Set(quality=>75);
	return $image;
}
