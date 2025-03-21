package com.chen.demo.service;

import com.chen.demo.model.AyUser;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.Collection;
import java.util.List;

/**
 * @InterfaceName AyUserService
 * @Description TODO
 * @Author newChenyingtao
 * @Date 2020/9/26 21:52
 * @Version 1.0
 */
public interface AyUserService {
    /**
     * id查询
     * @param id
     * @return
     */
    AyUser findById(Integer id);
    
    /**
     * 查找
     * @return
     */
    List<AyUser> findAll();
    
    /**
     * 存储用户
     * @param ayUser
     * @return
     */
    AyUser save(AyUser ayUser);
    
    /**
     * 删除功能
     * @param ayUser
     * @return
     */
    int delete(AyUser ayUser);
    
    /**
     * 分页查询功能
     * @param pageable
     * @return
     */
    Page<AyUser> findAll(Pageable pageable);
    
    /**
     * 查找姓名
     * @param name
     * @return
     */
    List<AyUser> findByName(String name);
    
    /**
     * 模糊查找姓名
     * @param name
     * @return
     */
    List<AyUser> findByNameLike(String name);
    
    /**
     * 批量查找id
     * @param id
     * @return
     */
    List<AyUser> findByIdIn(Collection<Integer> id);
    
    /**
     * 根据用户名和密码查询
     * @param name
     * @param password
     * @return
     */
    AyUser findByNameAndPassword(String name, String password);
}
