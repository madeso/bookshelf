+++
title = "Source code example"
weight = 30
+++

Some source code example [from linux](https://github.com/torvalds/linux/blob/master/fs/bfs/inode.c):

```c
struct inode *bfs_iget(struct super_block *sb, unsigned long ino)
{
	struct bfs_inode *di;
	struct inode *inode;
	struct buffer_head *bh;
	int block, off;

	inode = iget_locked(sb, ino);
	if (!inode)
		return ERR_PTR(-ENOMEM);
	if (!(inode->i_state & I_NEW))
		return inode;

	if ((ino < BFS_ROOT_INO) || (ino > BFS_SB(inode->i_sb)->si_lasti)) {
		printf("Bad inode number %s:%08lx\n", inode->i_sb->s_id, ino);
		goto error;
	}

	block = (ino - BFS_ROOT_INO) / BFS_INODES_PER_BLOCK + 1;
	bh = sb_bread(inode->i_sb, block);
	if (!bh) {
		printf("Unable to read inode %s:%08lx\n", inode->i_sb->s_id,
									ino);
		goto error;
	}

	off = (ino - BFS_ROOT_INO) % BFS_INODES_PER_BLOCK;
	di = (struct bfs_inode *)bh->b_data + off;

	inode->i_mode = 0x0000FFFF & le32_to_cpu(di->i_mode);
	if (le32_to_cpu(di->i_vtype) == BFS_VDIR) {
		inode->i_mode |= S_IFDIR;
		inode->i_op = &bfs_dir_inops;
		inode->i_fop = &bfs_dir_operations;
	} else if (le32_to_cpu(di->i_vtype) == BFS_VREG) {
		inode->i_mode |= S_IFREG;
		inode->i_op = &bfs_file_inops;
		inode->i_fop = &bfs_file_operations;
		inode->i_mapping->a_ops = &bfs_aops;
	}

	BFS_I(inode)->i_sblock =  le32_to_cpu(di->i_sblock);
	BFS_I(inode)->i_eblock =  le32_to_cpu(di->i_eblock);
	BFS_I(inode)->i_dsk_ino = le16_to_cpu(di->i_ino);
	i_uid_write(inode, le32_to_cpu(di->i_uid));
	i_gid_write(inode,  le32_to_cpu(di->i_gid));
	set_nlink(inode, le32_to_cpu(di->i_nlink));
	inode->i_size = BFS_FILESIZE(di);
	inode->i_blocks = BFS_FILEBLOCKS(di);
	inode->i_atime.tv_sec =  le32_to_cpu(di->i_atime);
	inode->i_mtime.tv_sec =  le32_to_cpu(di->i_mtime);
	inode->i_ctime.tv_sec =  le32_to_cpu(di->i_ctime);
	inode->i_atime.tv_nsec = 0;
	inode->i_mtime.tv_nsec = 0;
	inode->i_ctime.tv_nsec = 0;

	brelse(bh);
	unlock_new_inode(inode);
	return inode;

error:
	iget_failed(inode);
	return ERR_PTR(-EIO);
}
```
