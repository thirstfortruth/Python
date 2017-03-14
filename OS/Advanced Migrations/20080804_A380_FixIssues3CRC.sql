-- A380 Force MG 3 for 3 EDDs

declare @id_ds integer

-- 3442SAAC000003
set @id_ds = (select id_ds from r_fin_ds where substring(eddreference,1,14) = '3442SAAC000003')

update R_FIN_DS 
set 
 VALM2 ='Validated'
,MG='3'
where id_ds = @id_ds

UPDATE R_FIN_DS 
SET 
 EDDCheckSum = dbo.ELCOCHECK(@id_ds)
WHERE id_ds = @id_ds

-- 4411RHDC000433
set @id_ds = (select id_ds from r_fin_ds where substring(eddreference,1,14) = '4411RHDC000433')

update R_FIN_DS 
set 
 VALM2 ='Validated'
,MG='3' 
where id_ds = @id_ds

UPDATE R_FIN_DS 
SET 
 EDDCheckSum = dbo.ELCOCHECK(@id_ds)
WHERE id_ds = @id_ds

-- 4411RHDC000458
set @id_ds = (select id_ds from r_fin_ds where substring(eddreference,1,14) = '4411RHDC000458')

update R_FIN_DS 
set 
 VALM2 ='Validated'
,MG='3' 
where id_ds = @id_ds

UPDATE R_FIN_DS 
SET 
 EDDCheckSum = dbo.ELCOCHECK(@id_ds)
WHERE id_ds = @id_ds