```Python
resultSet = {}  // the blocks need to be accessed

main() {
    call timeIntervalQuery(ts, te);
    return resultSet;
}

timeIntervalQuery(ts, te) {
    Use array AT to find the time of the last object Y at time te. 
    Starting from Y go up recursively and then we get block P.
    call searchHelperFunction(ts, P);
}

searchHelperFunction(ts, block) {

    if( block == null ) {
        return ;
    }

    if( block.te >= ts ) {
        // report all the records in this block that were alive during [ts, te]
        resultSet.add(block);    
    } 
    else {
        return ;
    }
    
    searchHelperFunction(ts, block->rightmost_child);
    searchHelperFunction(ts, block->left_sibling);
}
```

I/O complexity: $O(\log_bn+N/b)$,
where $n$ is the number of all records and $N$ is the number of all real-world objects.
