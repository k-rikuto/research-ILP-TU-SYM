def follow_the_path(src:int, path:set[tuple[int,int,int]], visited:list[bool], finished:list[bool]) -> bool:
    visited[src-1] = True
    for link in path:
        v,u,c = link
        if v == src:
            if finished[u-1]: continue
            if visited[u-1] and not finished[u-1]: return True
            if follow_the_path(src=u,path=path,visited=visited,finished=finished): return True
    finished[src-1] = True
    return False


def check_cycle(r:tuple[int,int], path:set[tuple[int,int,int]], V:list[int]) -> bool:

    visited = [False for v in V]
    finished = [False for v in V]
    src,dest = r

    find = follow_the_path(src=src, path=path, visited=visited, finished=finished)

    return find

if __name__ == "__main__":
    path = set({(1,2,1),(2,3,1),(3,4,1),(4,2,1)})
    V = [1,2,3,4]
    r = (1,4)
    print(check_cycle(r=r, path=path, V=V))