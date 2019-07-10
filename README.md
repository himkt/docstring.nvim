# Docstring.nvim

Python docstring generator.

<img src="https://user-images.githubusercontent.com/5164000/60929694-5e075b00-a2ed-11e9-8f73-d628173391f4.gif" width="40%">

# Dependency

docstring.nvim currently depends on [Shougo/neosnippet.vim: neo-snippet plugin](https://github.com/Shougo/neosnippet.vim) to
expand and jump to a placeholder.

After installing and configuring neosnippet, we can jump to placeholders by `Ctrl-k`.

# Install

### vim-plug

```viml
Plug 'himkt/docstring.nvim', { 'do': ':UpdateRemotePlugins' }
```

### dein.vim

You may have to run `:UpdateRemotePlugins` manually.

```viml
call dein#add('Shougo/deoplete.nvim')
```
