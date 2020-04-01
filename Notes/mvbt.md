# Multiversion B-tree (MVBT)
Ziqi Tan
## Parameters
1. Block capacity $b = 6$.
2. Constant $k = 3$.
3. Constant $\epsilon = 0.5$.
4. Constant $b=kd$.

Assume the number of current entries is $N$.

### Block overflow
再插入元素的时候，当前的block A已经满了，然后就会对A进行version split，原来的Block A会死掉，得到新的block B和Block C.

如果现在还没有Root，就会生成一个Root block.

### Block underflow在这个Block没有发生删除的时候，是不会发生的。

### Weak version conditiion
$$N >= d \ || \ N = 0$$
#### Weak version Underflow
在这个Block发生删除的时候，当前的block A存活的节点数量少于d，那么这个block A就要执行version split，把还存活的值都放到一个新的block A*.

### Strong version condition 
which is used right after a version split or a merge:
$$ (1+\epsilon)d \le N \le (k-\epsilon)d$$

#### Strong version underflow
刚刚split产生的block的元素个数少于$(1+\epsilon)d$，这个时候就需要与一个sibling block进行merge操作。

#### Strong version overflow
发生merge操作后，当前block A的元素个数大于$(k-\epsilon)d$，这时候就会发生key split操作，将block A中的元素平分到两个新的blocks中，相应地，我们需要更新Root中的key.

#### Root没有Strong version underflow
