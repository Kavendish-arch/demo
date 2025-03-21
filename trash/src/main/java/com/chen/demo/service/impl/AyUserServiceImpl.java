package com.chen.demo.service.impl;

import com.chen.demo.dao.AyUserDao;
import com.chen.demo.model.AyUser;
import com.chen.demo.repository.AyUserRepository;
import com.chen.demo.service.AyUserService;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;

/**
 * @ClassName AyUserServiceImpl
 * @Description TODO
 * @Author newChenyingtao
 * @Date 2020/9/26 21:54
 * @Version 1.0
 */
@Transactional
@Service
public class AyUserServiceImpl implements AyUserService {
    
    @Resource
    private AyUserRepository ayUserRepository;
   
    @Resource
    private AyUserDao ayUserDao;
    
    @Override
    public AyUser findById(Integer id) {
        return ayUserRepository.findAllById(id);
    }
    
    @Override
    public List<AyUser> findAll() {
        return ayUserRepository.findAll();
    }
    
    @Override
    @Transactional
    public AyUser save(AyUser ayUser) {
        AyUser saveUser = ayUserRepository.save(ayUser);
        return saveUser;
    }
   
    @Override
    public int delete(AyUser ayUser) {
        ayUserRepository.delete(ayUser);
        return 0;
    }
    
    @Override
    public Page<AyUser> findAll(Pageable pageable) {
        return ayUserRepository.findAll(pageable);
    }
    
    @Override
    public List<AyUser> findByName(String name) {
        return ayUserRepository.findByUsername(name);
    }
    
    @Override
    public List<AyUser> findByNameLike(String name) {
        return ayUserRepository.findByUsernameLike(name);
    }
    
    @Override
    public List<AyUser> findByIdIn(Collection<Integer> id) {
        return ayUserRepository.findByIdIn(id);
    }
    
    @Override
    public AyUser findByNameAndPassword(String name, String password) {
        return ayUserDao.findByNameAndPassword(name, password);
    }
}
