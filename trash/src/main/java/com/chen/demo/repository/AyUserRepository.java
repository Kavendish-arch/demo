package com.chen.demo.repository;


import com.chen.demo.model.AyUser;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.transaction.annotation.Transactional;

import java.util.Collection;
import java.util.List;

/**
 * @ClassName AyUserRepository
 * @Description TODO
 * @Author newChenyingtao
 * @Date 2020/9/26 21:50
 * @Version 1.0
 */
public interface AyUserRepository extends JpaRepository<AyUser, Integer> {
    /**
     * 查找姓名
     * @param name
     * @return
     */
    List<AyUser> findByUsername(String name);
    
    /**
     * 根据id 查找
     * @param id
     * @return
     */
    AyUser findAllById(Integer id);
    /**
     * 模糊查找姓名
     * @param name
     * @return
     */
    List<AyUser> findByUsernameLike(String name);
    
    /**
     * 批量查找id
     * @param id
     * @return
     */
    List<AyUser> findByIdIn(Collection<Integer> id);
    
    /**
     * 通过id 删除用户
     * @param id
     * @return
     */
    int deleteAyUserById(Integer id);
    
    int deleteAyUsersByIdIn(Collection<Integer> ids);
}
